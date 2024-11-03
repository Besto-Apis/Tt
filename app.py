from flask import Flask, Response, request
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

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
    uid = request.args.get('Uid')
    password = request.args.get('Pw')

    if not uid or not password:
        return Response(" - Missing Uid or Pw!", status=400, mimetype='text/plain')

    # استخدام ThreadPoolExecutor لتحسين الأداء
    with ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(fetch_token, uid, password)
        result = future.result()

    return Response(result, mimetype='text/plain')

if __name__ == '__main__':
    app.run(threaded=True)
