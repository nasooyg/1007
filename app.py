import os
from flask import Flask, request, jsonify, render_template
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS 설정을 통해 프론트엔드와의 통신을 허용

# OpenAI API 키 설정 (환경 변수 사용)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def index():
    # 'talking GPT.html' 파일 렌더링
    return render_template('talking GPT.html')

@app.route('/chat', methods=['POST'])
def chat():
    # 클라이언트로부터 사용자 메시지를 받음
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # OpenAI GPT-3.5 Turbo API에 요청 보내기
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful private detective. Speak in 100 characters or less"},
                {"role": "user", "content": user_message}
            ],
            max_tokens=100,
            temperature=0.7
        )

        # GPT의 응답 추출
        bot_reply = response.choices[0].message['content'].strip()

        # 클라이언트에 응답 반환
        return jsonify({'reply': bot_reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 서버 실행 (디버그 모드 활성화)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 88)), debug=True)
