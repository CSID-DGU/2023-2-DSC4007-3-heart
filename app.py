from flask import Flask,render_template
from flask import request, jsonify
# from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
# CORS(app)

API_KEY = os.getenv("api_key")

#chat gpt api불러오기
client = OpenAI(
    api_key = API_KEY
)

# Function to complete chat input using OpenAI's GPT-3.5 Turbo
def chatcompletion(user_input):
    output = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": f"{user_input}."},
        ]
    )

    print(output)
    chatgpt_output = output.choices[0].message.content#gpt 답변
    print(chatgpt_output)
    return chatgpt_output 

# Function to handle user chat input
def chat(user_input):
    chatgpt_raw_output = chatcompletion(user_input)
    return chatgpt_raw_output 

# Function to get a response from the chatbot
def get_response(userText):
    return chat(userText)

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    options = ["1.생활지원", "2.주거지원", "3.건강의료", "4.고용,일자리", "5.돌봄", "6.기타"]
    
    if userText in options:
        return f"{userText}을 선택하셨습니다."
    elif "홍길동" in userText:
        return f"신원확인 되었습니다. 궁금하신 사항을 구체적으로 말씀해주세요. "
    elif "홍길동" in userText and "-" in userText:
        return f"잘못된 정보입니다. 다시 입력해주세요."
    else:
        return chatcompletion(userText)

# Run the Flask app
if __name__ == "__main__":
    app.run()