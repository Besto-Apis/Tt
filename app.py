from flask import Flask, Response
import requests
import json

app = Flask(__name__)

def load_tokens():
    url = "https://raw.githubusercontent.com/Besto-Apis/Tt/refs/heads/main/Tokens.txt"
    response = requests.get(url)
    if response.status_code == 200:
        tokens_dict = json.loads(response.text)
        return [(uid, pw) for uid, pw in tokens_dict.items()]
    return []

def fetch_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067",
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        NEW_ACCESS_TOKEN = result['access_token']
        NEW_OPEN_ID = result['open_id']
        return f" - Access Token : {NEW_ACCESS_TOKEN}\n - Access Id : {NEW_OPEN_ID}\n\n"
    except Exception as e:
        return f" - Error In Uid {uid}: {str(e)}"

@app.route('/Token', methods=['GET'])
def get_token():
    tokens = load_tokens()
    if not tokens:
        return Response(" - Failed to load tokens!", status=500, mimetype='text/plain')

    results = []
    for uid, password in tokens:
        result = fetch_token(uid, password)
        results.append(result)
        
        # يمكن إرجاع النتائج كلما كانت القائمة تحتوي على عدد معين من النتائج
        if len(results) >= 10:  # على سبيل المثال، كل 10 نتائج
            yield Response("\n".join(results), mimetype='text/plain')
            results.clear()  # مسح النتائج لتخزين جديدة

    # إرجاع أي نتائج متبقية
    if results:
        return Response("\n".join(results), mimetype='text/plain')

    return Response(" - No tokens processed.", status=204)

if __name__ == '__main__':
    app.run(threaded=True)
