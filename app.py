import os
import uuid
from flask import Flask, request, jsonify, render_template, session
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# OpenAI API 키 설정 (환경 변수 사용)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 세션을 위한 secret key 설정
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key_here")


@app.route("/")
def index():
    # 학생에게 고유 세션 ID 부여
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        session["conversation"] = []  # 개별 대화 기록 초기화
    return render_template("talking GPT.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # 세션 ID를 기반으로 학생의 대화 이력 관리
    conversation = session.get("conversation", [])
    conversation.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a  helpful private detective. Speak in 100 characters or less",
                }
            ]
            + conversation,
            max_tokens=100,
            temperature=0.7,
        )

        bot_reply = response.choices[0].message["content"].strip()
        conversation.append({"role": "assistant", "content": bot_reply})

        # 갱신된 대화 이력 세션에 저장
        session["conversation"] = conversation

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
