from flask import Flask, request
from dotenv import load_dotenv
import os
import openai


app = Flask(__name__)
load_dotenv()

base_prompt = os.getenv("BASE_INSTRUCTIONS")
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/answer', methods=['POST'])
def answer():
    question = request.get_json().get('question')
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": question}
        ]
    )
    return completion.choices[0].message


if __name__ == '__main__':
    app.run(debug=True)
