from flask import Flask, render_template_string
import requests

app = Flask(__name__)

TEAMVIEWER_TOKEN = "26256879-559hW5ZrSkPgJCIUI22k"
API_URL = "https://webapi.teamviewer.com/api/v1/sessions"

@app.route("/")
def create_session():
    headers = {
        "Authorization": f"Bearer {TEAMVIEWER_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "groupname": "자동 생성 그룹",
        "description": "Python 서버 테스트",
        "end_customer": {
            "name": "홍길동",
            "email": "hong@example.com"
        },
        "support_session_type": "Default"
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload)
        data = res.json()
        session_link = data.get("end_customer_link")
    except Exception as e:
        session_link = None

    return render_template_string("""
    <html>
      <head><title>TeamViewer 원격 세션</title></head>
      <body style="font-family: sans-serif; text-align: center; padding-top: 100px;">
        {% if session_link %}
          <h2>✅ 세션이 생성되었습니다!</h2>
          <p><a href="{{ session_link }}" target="_blank">{{ session_link }}</a></p>
          <button onclick="navigator.clipboard.writeText('{{ session_link }}'); alert('복사되었습니다!')">🔗 복사하기</button>
        {% else %}
          <h2>❌ 세션 생성 실패</h2>
        {% endif %}
      </body>
    </html>
    """, session_link=session_link)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
