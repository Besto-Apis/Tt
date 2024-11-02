from flask import Flask, Response
import requests
import json
import firebase_admin
from firebase_admin import credentials, firestore
import asyncio
import concurrent.futures

app = Flask(__name__)

# إعداد Firebase
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "bot-ff-ce808",
    "private_key_id": "2de18bf0a5522000e38bdbe8384e95f7768587d2",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC85sphD9j12e0q\nfG8wvnTGSSpqeh4s3PSCHe29VWkvYYFHBkgG2iDLLUlmDntLF6Bb50wg/63iH6w8\ne9SwH53BeqM3SHX4pYX7GSQ4wkPiESws82dUSvdJHeiof7jNKA+salO5CmWm8Y0/\nHpI0j59ERQmDT5SnyLvE6FAKryxyn2Rky3FnHYUAPC8Aj6PZqLpgeWeN67QbvU7Z\n9ZZMB/EFtvx7xWuFnR/GWlv6GdoyPpqiNIoR9fCyUhqRyDQlyAmhwFws9BQx11O1\nVTx7YZ/8Jc+plXRi39HnYZsc3RYXAojqNFdgdFXr8aZgCTxfibGgYSwUg1sq9YWp\no351AcqrAgMBAAECggEAC1pIyhHhwCTGFB+WWcpDH7JAp6rfKrhnbsp4V0Ci1FjP\nzteZzI+fbkEygBJZZpHs7pkKrOZbf5OCY8AtcB2g+tfGp16Qzc4PgfUThYsR+VbU\nM39is7Ytq79DFEgDcJD6dX+OYziKE2vA9AzU90O1Fq1E0mzIn6zOBsTPdVTsdEGg\nSOSuIjb1xH3fWNj22JDsdn9roysWt/y4/jurVcarzUxzJ4pc7CW4UFCuR9fDpwVN\nUewEXTZ8/n22CJ1lvEIa3RZGpFHqM2JVXZ8BKrWW9u26QQ3cWQyt+LhoML7ltayc\nmlK9A4ng/q63kMuLwRPT4Zvax8Cs7NKsxqxqB+LFAQKBgQDhYXl3lEt0A3cNghYg\nEz8FNjS+SZ5f27HjvJOnMOsEe/sI03qSyPo2LjT41XxTPNl7AmA7r9cGJSOBjEoQ\nIbNkHGTuB/0IbvY013VGAn8/z4lXylVofkGG6Ant4PwPRfJ1m47CCm6pBykmUEft\nXBuiLVxkPuE3fG1ETu036OeG8QKBgQDWkJp9GhKLTaYz8xoIcSb/YrFevg77p6Rm\nao4z/rsRBlaHEgIbY+VaNaIZRdjsbqj1NdddNZB5OGyG7mQTcUkMLnKWL9koMEyI\nbJVWuqeu6p3HKRQw4cdC2MvrCSd/Jzo38qeIct2wfzvf8Qw8Vyw4sZsdOOWa6wxl\n1o/AdiADWwKBgAsREDfQ7kuKCAR/yLpWd5e366sUTlSCox99mPpyqneT5uWuDKy8\ndZzHdA5r3SjxKfSiTztfDP3eQPoRe2mDXh2iT0po1gHeAPTjR3zijoEBncrTwpHY\n8TrAlgw6KeZOFvOzabUZcgmWsmyRMJb1GN5Dv++kLsbcszjRb1B5fTThAoGBAJcK\nWBY0olU5pgPv36WNsbwZh26AMB/q1QnbfJsReDH12jde7+jEG5GzK5bK2nclNv7W\nlfJhYIBUveEGM6CUIK3YjIU4zY9C4L0wYrgY0S2KruKiAjqe1RwzbOjZGtqhjJQR\n1ulwoqo6BrYQA2L+onyOWfjqMocpayLNNYhwHvz9AoGALfNwOPg8Wmufx9Ok8ocF\nMLfnuGzj7+bc/AMTzLvyLzTffFH5dpdtCuP/a9Y7vvrL29og2V20g8/kSByFIrmo\nsraSZyPGUZxztcOQ7epIJr/uFAUsWTrPR3GCCpJJf7tvA5MamUWxqV4iiBRqqJwy\n9VepexXDZwnaSN/ZxQC35kY=\n-----END PRIVATE KEY-----\n",
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

def load_tokens():
    url = "https://raw.githubusercontent.com/Besto-Apis/Tt/refs/heads/main/Tokens.txt"
    response = requests.get(url)
    if response.status_code == 200:
        tokens_dict = json.loads(response.text)
        return [(uid, pw) for uid, pw in tokens_dict.items()]
    return []

async def fetch_token(uid, password):
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
        
        # حفظ التوكن في Firestore
        db.collection('tokens').add({
            'uid': uid,
            'access_token': NEW_ACCESS_TOKEN,
            'open_id': NEW_OPEN_ID
        })
        
        return f" - Access Token : {NEW_ACCESS_TOKEN}\n - Access Id : {NEW_OPEN_ID}\n\n"
    except Exception as e:
        return f" - Error In Uid: {uid} | {str(e)}\n\n"

@app.route('/Token', methods=['GET'])
async def get_token():
    tokens = load_tokens()
    if not tokens:
        return Response(" - Failed to load tokens!", status=500, mimetype='text/plain')

    async def generate_results():
        for uid, password in tokens:
            result = await fetch_token(uid, password)
            yield result

    return Response(generate_results(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(threaded=True)
