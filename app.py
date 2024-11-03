from flask import Flask, Response
import aiohttp
import asyncio
import json

app = Flask(__name__)

async def fetch_token(session, uid, password):
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

    async with session.post(url, headers=headers, data=data) as response:
        if response.status == 200:
            result = await response.json()
            return f" - Access Token : {result['access_token']}\n - Access Id : {result['open_id']}\n\n"
        else:
            return f" - Error In Uid {uid}!"

async def generate_results(tokens):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_token(session, uid, password) for uid, password in tokens]
        return await asyncio.gather(*tasks)

@app.route('/Token', methods=['GET'])
async def get_token():
    tokens = load_tokens()
    if not tokens:
        return Response(" - Failed to load tokens!", status=500, mimetype='text/plain')

    results = await generate_results(tokens)
    return Response("\n".join(results), mimetype='text/plain')

def load_tokens():
    url = "https://raw.githubusercontent.com/Besto-Apis/Tt/refs/heads/main/Tokens.txt"
    response = requests.get(url)
    if response.status_code == 200:
        tokens_dict = json.loads(response.text)
        return [(uid, pw) for uid, pw in tokens_dict.items()]
    return []

if __name__ == '__main__':
    app.run(threaded=True)
