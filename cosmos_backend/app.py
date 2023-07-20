from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship
import json
from flask_bcrypt import Bcrypt
import jwt
import time

app = Flask(__name__)
load_dotenv()
bcrypt = Bcrypt(app)

admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")
base_prompt = os.getenv("BASE_INSTRUCTIONS")
openai.api_key = os.getenv("OPENAI_API_KEY")
connection_string = os.getenv("CONNECTION_STRING_MYSQL")
engine = create_engine(connection_string, echo=True)
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

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True)
    user_chat_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(200))

Base.metadata.create_all(engine)

# middleware

@app.before_request
def check_authorization():
    if request.endpoint in ["user_question", "user_chat-history_<int:user_id>"]:
        if not request.headers.get("Authorization"):
            return "Unauthorized", 401
        else:
            try:
                payload = jwt.decode(request.headers.get("Authorization"), secretKey, algorithms=["HS256"])
                email = payload["email"]
                request.environ["email_from_token"] = email
            except jwt.ExpiredSignatureError:
                return "JWT token has expired.", 401
            except Exception as e:
                print(e)
                return "Invalid JWT token.", 401
    elif request.endpoint in ["admin_chat", "/admin_feedback"]:
        if not request.headers.get("Authorization"):
            return "Unauthorized", 401
        else:
            try:
                payload = jwt.decode(request.headers.get("Authorization"), secretKeyADMIN, algorithms=["HS256"])
                email = payload["email"]

                if request.data is not None:
                    request.data.update({"email": email})
                else:
                    request.data = {"email": email}
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
                {"email": data["email"], "exp": expiration_timestamp}, secretKey, algorithm="HS256")
             return jsonify({"message": "Login successful!", "user_id": user.id, "token": encoded_jwt}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
        
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Admin Login
@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    if admin["email"] == data["email"] and admin["password"] == data["password"]:
        expiration_timestamp = int(time.time()) + expiration_time_seconds
        encoded_jwt = jwt.encode({"email": data["email"], "exp": expiration_timestamp}, secretKeyADMIN, algorithm="HS256")
        return jsonify({"message": "Admin login successful!", "token": encoded_jwt}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# User Question Route with User Chat ID
@app.route('/user/question', methods=['POST'])
def user_question():
    email = request.environ.get("email_from_token")
    data = request.json
    user_id = data["user_id"]
    user_chat_id = data["user_chat_id"]
    question = data["question"]
    session = Session()
    user_chat = session.query(UserChat).filter_by(id=user_chat_id, user_id=user_id).first()

    if user_chat:
        chat_thread = json.loads(user_chat.chat_thread)
        chat_thread.insert(0, {"role": "system", "content": base_prompt})
        chat_thread.append({"role": "user", "message": question})

        # Perform the GPT-3 completion as before
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_thread
        )
        chat_thread.append(completion.choices[0].message)
        chat_thread.pop(0)

        user_chat.chat_thread = json.dumps(chat_thread)
        session.commit()
        session.close()
        return jsonify({"message": "Question sent successfully!", "response": completion.choices[0].message}), 200
    else:
        session.close()
        return jsonify({"error": "User chat not found"}), 404
    
# User Chat History Get Route
@app.route('/user/chat-history/<int:user_id>', methods=['GET'])
def user_chat_history(user_id):
    session = Session()
    user_chats_history = session.query(UserChat).filter_by(user_id=user_id).all()
    session.close()
    user_chats_history = [
        {
            "id": user_chat.id,
            "user_id": user_chat.user_id,
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
    user_chat_id = data["user_chat_id"]
    rating = data["rating"]
    comment = data["comment"]

    session = Session()
    user_chat = session.query(UserChat).filter_by(id=user_chat_id).first()
    if user_chat:
        user_chat.is_feedback_given = True
        feedback = Feedback(user_chat_id=user_chat_id, rating=rating, comment=comment)
        session.add(feedback)
        session.commit()
        session.close()
        return jsonify({"message": "Feedback submitted successfully!"}), 200
    else:
        session.close()
        return jsonify({"error": "User chat not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
