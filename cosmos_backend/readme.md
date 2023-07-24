# Flask Chat Application

This is a Flask-based chat application that allows users to sign up, log in, and interact with an AI-powered chatbot. The application also provides an admin interface to view and manage user chat history and feedback.

## Getting Started

To run the application on your local machine, follow these steps:

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Set up environment variables:
   - Create a `.env` file in the project root directory.
   - Add the following environment variables to the `.env` file:

    ```
    ADMIN_EMAIL=<admin-email>
    ADMIN_PASSWORD=<admin-password>
    BASE_INSTRUCTIONS=<base-prompt>
    OPENAI_API_KEY=<openai-api-key>
    CONNECTION_STRING_MYSQL=<mysql-connection-string>
    SUPER_SECRET_KEY=<secret-key>
    SUPER_SECRET_KEY_ADMIN=<admin-secret-key>
    final_chat=<fine tune the answer prompt>
    ```

   Replace the placeholders (`<...>`) with your actual values.

5. Run the application: `python app.py`

The application should now be running on `http://127.0.0.1:5000`.

## Endpoints

The application provides the following endpoints:

### User Endpoints

1. **Sign Up**: `/signup` [POST]
   - Create a new user account.
   - Request Body: `{"name": "user-name", "email": "user-email", "password": "user-password"}`
   - Response: `{"message": "User created successfully!"}`

2. **Log In**: `/login` [POST]
   - Log in with a registered user account and receive a JWT token.
   - Request Body: `{"email": "user-email", "password": "user-password"}`
   - Response: `{"message": "Login successful!", "user_id": 1, "name": "user-name", "token": "jwt-token"}`

### Admin Endpoints

1. **Admin Log In**: `/admin_login` [POST]
   - Log in as an admin user and receive a JWT token.
   - Request Body: `{"email": "admin-email", "password": "admin-password"}`
   - Response: `{"message": "Admin login successful!", "token": "jwt-token"}`

2. **Get Chat Threads without Feedback**: `/admin/chat` [GET]
   - Retrieve chat threads without feedback from users.
   - Requires Admin JWT token in the Authorization header.
   - Response: `{"chat_threads": [...]}`

3. **Submit Feedback**: `/admin/feedback` [POST]
   - Submit feedback for a user chat thread.
   - Requires Admin JWT token in the Authorization header.
   - Request Body: `{"user_chat_id": 1, "rating": 4, "comment": "feedback-comment"}`
   - Response: `{"message": "Feedback submitted successfully!"}`

4. **Get All Feedback**: `/admin/all_feedback` [GET]
   - Retrieve all feedback along with the associated chat thread.
   - Requires Admin JWT token in the Authorization header.
   - Response: `{"feedback_with_chat_thread": [...]}`

### User Chat Endpoints

1. **Send User Question**: `/user/question` [POST]
   - Send a question to the AI chatbot and receive a response.
   - Requires User JWT token in the Authorization header.
   - Request Body: `{"user_chat_id": 1, "question": "user-question"}`
   - Response: `{"message": "Question sent successfully!", "response": "bot-response"}`

2. **Get User Chat History**: `/user/chat_history` [GET]
   - Retrieve the chat history for the current user.
   - Requires User JWT token in the Authorization header.
   - Response: `{"user_chat_history": [...]}`

## Middleware

The application implements a middleware function `check_authorization()` to ensure that only authorized users can access specific endpoints. The middleware performs JWT token verification and sets environment variables for further request processing.

## Database Models

The application uses SQLAlchemy to define the following database models:

1. `User`: Represents a user account with attributes `id`, `name`, `email`, `password`, and `profile_image`.
2. `UserChat`: Represents a user chat thread with attributes `id`, `user_id`, `chat_thread`, `is_feedback_given`, and `created_at`.
3. `Feedback`: Represents user feedback with attributes `id`, `user_chat_id`, `rating`, and `comment`.

<a href="https://ibb.co/D86fK4Q"><img src="https://i.ibb.co/F0f476z/ER.png" alt="ER" border="0"></a><br /><a target='_blank' href='https://imgbb.com/'>editor de fotos tumblr</a><br />

## Note

Please note that this application is for demonstration purposes and may require additional security and error handling for production use. Additionally, it is assumed that the database has already been set up with the appropriate tables based on the defined models.

Feel free to explore and modify the code to suit your specific use case. Happy coding!
