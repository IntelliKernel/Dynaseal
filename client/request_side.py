import json
from time import sleep
import requests

backend_url = "http://localhost:9000/api/v1"
llm_server_url = "http://localhost:8000/api/v1"

# login
email = "client1@example.com"
password = "client1"
login_headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}

login_data = {
    "grant_type": "password",
    "username": email,
    "password": password,
    "scope": "",
    "client_id": "string",
    "client_secret": "string",
}
response = requests.post(
    backend_url + "/user/login", headers=login_headers, data=login_data
).json()

login_token = response["access_token"]

# get token
get_token_headers = {
    "Authorization": "Bearer " + login_token,
}

client_token = requests.post(
    backend_url + "/key/create", headers=get_token_headers
).json()


token = client_token["token"]

header = {"dynasealtoken": token}

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who are you?"},
    ],
    "max_tokens": 100,
    "temperature": 0.6,
    "top_p": 0.9,
    "stream": True,
}


response = requests.post(
    llm_server_url + "/client-side/chat/completions",
    headers=header,
    json=payload,
    stream=True,
)
# print(response.json())
# for message in response:
#     print(message, end="", flush=True)

if response.status_code == 200:
    for line in response.iter_lines():
        if line:
            print(
                json.loads(line.decode("utf-8")[6:])["choices"][0]["delta"]["content"],
                end="",
                flush=True,
            )
else:
    print(response.json())
