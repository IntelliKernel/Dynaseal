import requests

backend_url = "http://localhost:8000/api/v1"

email = "user1@example.com"
password = "user1"
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

token = response["access_token"]
print(token)

# get token
headers = {
    "Authorization": "Bearer " + token,
}

response = requests.post(backend_url + "/api_key/create", headers=headers).json()
print(response)
