from flask import Flask, request, jsonify, make_response
import openai
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import sessionmaker, relationship, load_only
import json
from flask_bcrypt import Bcrypt
import jwt
import time
from datetime import datetime
from flask_cors import CORS, cross_origin
from functools import wraps

load_dotenv()
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

bcrypt = Bcrypt(app)

admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")
base_prompt = os.getenv("BASE_INSTRUCTIONS")
final_prompt = os.getenv("final_chat")
openai.api_key = os.getenv("OPENAI_API_KEY")
connection_string = os.getenv("CONNECTION_STRING_MYSQL")
engine = create_engine(connection_string, echo=True, connect_args={'connect_timeout': 60})
Session = sessionmaker(bind=engine)
secretKey = os.getenv("SUPER_SECRET_KEY")
secretKeyADMIN = os.getenv("SUPER_SECRET_KEY_ADMIN")

expiration_time_seconds = 3600 #1 hour

admin = {"email": admin_email, "password": admin_password}

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    profile_image = Column(String(200))

class UserChat(Base):
    __tablename__ = 'user_chats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    chat_thread = Column(Text, nullable=False)
    is_feedback_given = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True)
    user_chat_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(200))

Base.metadata.create_all(engine)

def _build_cors_preflight_response():
    response = make_response()
    response.status_code = 200
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

# middleware

@app.before_request
def check_authorization():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    if request.endpoint in ["user_question", "user_chat_history"]:
        if not request.headers.get("Authorization"):
            return "Unauthorized", 401
        else:
            try:
                payload = jwt.decode(request.headers.get("Authorization"), secretKey, algorithms=["HS256"])
                email = payload["email"]
                id = payload["user_id"]
                request.environ["email_from_token"] = email
                request.environ["user_id_from_token"] = id
            except jwt.ExpiredSignatureError:
                return "JWT token has expired.", 401
            except Exception as e:
                print(e)
                return "Invalid JWT token.", 401
    elif request.endpoint in ["admin_get_chat", "admin_feedback", "admin_all_feedback"]:
        if not request.headers.get("Authorization"):
            return "Unauthorized", 401
        else:
            try:
                payload = jwt.decode(request.headers.get("Authorization"), secretKeyADMIN, algorithms=["HS256"])
                email = payload["email"]
                request.environ["email_from_token"] = email    
            except jwt.ExpiredSignatureError:
                return "JWT token has expired.", 401
            except Exception as e:
                return "Invalid JWT token.", 401


# User Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    pw_hash = bcrypt.generate_password_hash(data["password"])
    new_user = User(name=data["name"], email=data["email"], password=pw_hash, profile_image="dummy")
    session = Session()
    session.add(new_user)
    session.commit()
    session.close()
    return jsonify({"message": "User created successfully!"}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    session = Session()
    user = session.query(User).filter_by(email=data["email"]).first()
    session.close()
    if user:
        isCorrectPassword = bcrypt.check_password_hash(user.password, data["password"])
        if isCorrectPassword:
             expiration_timestamp = int(time.time()) + expiration_time_seconds
             encoded_jwt = jwt.encode(
                {"email": data["email"],"user_id": user.id, "exp": expiration_timestamp}, secretKey, algorithm="HS256")
             return jsonify({"message": "Login successful!", "user_id": user.id, "name": user.name, "token": encoded_jwt}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
        
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Admin Login
@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.json
    if admin["email"] == data["email"] and admin["password"] == data["password"]:
        expiration_timestamp = int(time.time()) + expiration_time_seconds
        encoded_jwt = jwt.encode({"email": data["email"], "exp": expiration_timestamp}, secretKeyADMIN, algorithm="HS256")
        return jsonify({"message": "Admin login successful!", "token": encoded_jwt}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# @app.route('/user/question', methods=['OPTIONS'])
# def preflight_user_question():
#     return _build_cors_preflight_response()

@app.route('/user/question', methods=['POST'])
def user_question():
    email_from_token = request.environ.get("email_from_token")
    data = request.json
    user_id = request.environ.get("user_id_from_token")
    user_chat_id = data.get("user_chat_id")  # Use get() to handle the case when user_chat_id is not provided
    question = data["question"]

    # If user_chat_id is not provided, create a new UserChat entry
    if not user_chat_id:
        session = Session()
        new_user_chat = UserChat(user_id=user_id, chat_thread="[]")  # Initialize an empty chat_thread
        session.add(new_user_chat)
        session.commit()
        user_chat_id = new_user_chat.id  # Use the generated user_chat_id
        session.close()

    chat_thread = [{"role": "system", "content": base_prompt}]

    if user_chat_id:
        session = Session()
        user_chat = session.query(UserChat).options(load_only(UserChat.chat_thread)).filter_by(id=user_chat_id, user_id=user_id).first()
        if user_chat:
            chat_thread = json.loads(user_chat.chat_thread)
        session.close()

    chat_thread.append({"role": "user", "content": question})

    # Perform the first GPT-3 completion to get the initial response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_thread,
    )
    initial_response = completion.choices[0].message["content"]

    # Create a new chat_thread with the initial response for the second GPT-3 completion
    chat_thread_with_response = chat_thread.copy()
    chat_thread_with_response.append({"role": "assistant", "content": initial_response})
    chat_thread_with_response.append({"role": "user", "content": final_prompt})

    # Perform the second GPT-3 completion with the initial response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_thread_with_response,
    )

    # Update the chat_thread attribute with the final response and commit the changes
    final_response_content = response.choices[0].message["content"]
    chat_thread_with_response[-2]["content"] = final_response_content
    chat_thread_with_response.pop(-1)

    session = Session()
    user_chat = session.query(UserChat).filter_by(id=user_chat_id, user_id=user_id).first()
    if user_chat:
        user_chat.chat_thread = json.dumps(chat_thread_with_response)
        session.commit()
    session.close()

    # Return only the user_chat_id and chat_thread in the response
    response_data = {
        "id": user_chat_id,
        "chat_thread": chat_thread_with_response,
    }
    return jsonify(response_data), 200



    
# @app.route('/user/chat-history', methods=['OPTIONS'])
# @cross_origin(headers=["Content-Type", "Authorization"])
# def preflight_chat_history():
#     return '', 204
    
# User Chat History Get Route
@app.route('/user/chat_history', methods=['GET'])
def user_chat_history():
    email_from_token = request.environ.get("email_from_token")
    user_id_from_token = request.environ.get("user_id_from_token")
    session = Session()
    user_chats_history = session.query(UserChat).filter_by(user_id=user_id_from_token).order_by(UserChat.id.desc()).all()
    session.close()
    user_chats_history = [
        {
            "id": user_chat.id,
            "chat_thread": json.loads(user_chat.chat_thread),  # Deserialize the JSON data
            "is_feedback_given": user_chat.is_feedback_given
        }
        for user_chat in user_chats_history
    ]
    
    return jsonify(user_chats_history), 200

# Admin Get Chat Route (Chat Threads without Feedback)
@app.route('/admin/chat', methods=['GET'])
def admin_get_chat():
    session = Session()
    chat_threads_without_feedback = session.query(UserChat).filter_by(is_feedback_given=False).all()
    session.close()
    chat_threads_without_feedback = [
        {
            "id": chat.id,
            "user_id": chat.user_id,
            "chat_thread": json.loads(chat.chat_thread),  # Deserialize the JSON data
            "is_feedback_given": chat.is_feedback_given
        }
        for chat in chat_threads_without_feedback
    ]
    return jsonify(chat_threads_without_feedback), 200

# Admin Feedback Route
@app.route('/admin/feedback', methods=['POST'])
def admin_feedback():
    data = request.json
    user_chat_id = data.get("user_chat_id")
    rating = data.get("rating")
    comment = data.get("comment")

    if user_chat_id is None:
        return jsonify({"error": "User chat id found"}), 404

    session = Session()
    user_chat = session.query(UserChat).filter_by(id=user_chat_id).first()
    if user_chat:
        if rating is not None and comment is not None:
            user_chat.is_feedback_given = True
            feedback = Feedback(user_chat_id=user_chat_id, rating=rating, comment=comment)
            session.add(feedback)
        elif rating is not None:
            user_chat.is_feedback_given = True
            feedback = Feedback(user_chat_id=user_chat_id, rating=rating, comment ="")
            session.add(feedback)
        elif comment is not None:
            user_chat.is_feedback_given = True
            feedback = Feedback(user_chat_id=user_chat_id, rating=0, comment=comment)
            session.add(feedback)
        else:
            # In case neither rating nor comment is provided, we can return an error or take appropriate action.
            # For now, I'll just return a message indicating that at least one of them should be provided.
            return jsonify({"error": "Please provide at least a rating or a comment."}), 400

        session.commit()
        session.close()
        return jsonify({"message": "Feedback submitted successfully!"}), 200
    else:
        session.close()
        return jsonify({"error": "User chat not found"}), 404
    
@app.route('/admin/all-feedback', methods=['GET'])
def admin_all_feedback():
    session = Session()
    feedback_data = session.query(Feedback).all()
    session.close()

    feedback_with_chat_thread = []
    for feedback in feedback_data:
        user_chat_id = feedback.user_chat_id
        user_chat = session.query(UserChat).filter_by(id=user_chat_id).first()
        if user_chat:
            feedback_with_chat_thread.append({
                "user_chat_id": user_chat_id,
                "rating": feedback.rating,
                "comment": feedback.comment,
                "chat_thread": json.loads(user_chat.chat_thread),
            })
        else:
            # Handle the case where the user chat associated with the feedback is not found.
            # You can take appropriate action here, like skipping the feedback or logging the issue.
            pass

    return jsonify(feedback_with_chat_thread), 200



if __name__ == '__main__':
    app.run(debug=True)
