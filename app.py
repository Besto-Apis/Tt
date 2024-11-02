from flask import Flask, Response
import requests
import json
import firebase_admin
from firebase_admin import credentials, firestore

# إعداد تطبيق Firebase
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "bot-ff-ce808",
    "private_key_id": "2de18bf0a5522000e38bdbe8384e95f7768587d2",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC85sphD9j12e0q\n... (key truncated for brevity)\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-hyjvw@bot-ff-ce808.iam.gserviceaccount.com",
    "client_id": "116844755629790343548",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-hyjvw%40bot-ff-ce808.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

def load_tokens():
    url = "https://raw.githubusercontent.com/Besto-Apis/Tt/refs/heads/main/Tokens.txt"
    response = requests.get(url)
    if response.status_code == 200:
        tokens_dict = json.loads(response.text)
        return [(uid, pw) for uid, pw in tokens_dict.items()]
    return []

@app.route('/Token', methods=['GET'])
def get_token():
    tokens = load_tokens()
    if not tokens:
        return Response(" - Failed to load tokens!", status=500, mimetype='text/plain')

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
        except requests.exceptions.RequestException as e:
            return f" - Error processing UID {uid}: {str(e)}\n\n"

    results = []
    for uid, password in tokens:
        result = fetch_token(uid, password)
        results.append(result)

    return Response(''.join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run(threaded=True)
