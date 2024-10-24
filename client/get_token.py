import requests

backend_url = "http://localhost:9000/api/v1"

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

print(client_token["token"])
