# Dynaseal

[中文](https://github.com/IntelliKernel/Dynaseal/blob/main/README_cn.md)

## Why This Project Exists

Imagine a future where LLM agents are fully deployed on the client-side. However, currently, calling large models is done through an API key that can be used freely once obtained. Wouldn’t that mean users could grab the API key from the client-side models and rack up your bill?!!! If every phone is running multiple agents, and you have a large number of users, wouldn’t your servers be worse off than being hit by a DDoS attack? Because a DDoS prevents you from providing services, but in this case, your regular business is still running while you're being overwhelmed!

Therefore, we’ve proposed Dynaseal, a server-side framework designed for future client-side agent model calls. It uses a dynamic token similar to OSS, limiting the models and parameters the client-side agents can call and controlling token lifespan. It allows client-side agents to communicate directly with large model service providers and notifies your business backend through a callback after the response is complete. We welcome feedback and star.

> Please note that this project is just a demo, implementing our design for dynamically distributing API keys from the client side to request large model responses. The large model part is designed as a wrapper for a large model server in the format of the OpenAI API. For client-side requests, we only perform simple key integrity checks and parameter validation. The callback for the end of the request only implements printing to the terminal.

## System Design

The architecture is divided into three parts: the LLM server, the backend, and the client.

1. **Backend Initialization**: The backend requests a large model API key from the LLM server.
2. **Client Initialization**: The client requests authentication from the backend's business interface. After passing, the backend returns a dynamic key, specifying the model, token, request address, and other basic information.
3. **Client Requests Model**: The client uses the dynamic key to request the model from the large model server.
4. **LLM Server Processes Request**: The LLM server unpacks the dynamic key, determines the identity, and generates and returns the response.
5. **LLM Server Notifies Backend**: The LLM server notifies the backend of the client's request and response through a callback.

![](https://cdn.studyinglover.com/pic/2024/10/e29ae616dcd9ea47249028aa91645930.png)

```mermaid
sequenceDiagram
    participant 后端 as 后端
    participant 客户端 as 客户端
    participant LLM服务端 as LLM服务端

    Note over 后端: 初始化
    后端->>LLM服务端: 请求大模型api-key
    LLM服务端-->>后端: 返回api-key

    Note over 客户端: 初始化
    客户端->>后端: 请求业务鉴权
    后端-->>客户端: 返回动态key, 包括可调用的模型, token等

    客户端->>LLM服务端: 使用动态key请求模型
    LLM服务端->>LLM服务端: 解包动态key, 确定身份
    LLM服务端-->>客户端: 返回响应

    LLM服务端->>后端: 通知客户端的请求和响应

```

## Dynamic Key Design

The dynamic key is designed as a JWT token, i.e., `header.payload.secret`.

- **header**
- **payload**: First, generate a JSON in the following format, then package it into the JWT payload.

```json
{
  "api-key": 111, // ID of the user registered by the backend on the LLM server, note that it is the ID, not the key given by the LLM server
  "model": "deepseek-chat", // Model name that the client side can call
  "max_tokens": 100, // Maximum number of tokens that can be called
  "expiring": 111, // Expiration time, using Unix timestamp
  "event_id": 111 // Event ID, used to represent this token, the LLM server will include this event_id in the response after completing the request
}
```

- **secret**: Encrypted using the key obtained by the backend from the LLM server, the LLM server will use this part to verify the legality of the dynamic key.

## Implementation Details

### Folder Explanation

- **llm-server**: The large model backend, the server we usually call in normal use, with our design added on top of the regular API calls—authentication and response for dynamic keys.
- **backend**: The business backend, the backend provided by companies/individuals who have purchased the large model API key, which can authenticate the client side and then distribute dynamic keys.
- **client**: The client side, where agents run.

### Database Creation

#### LLM Server

Create a user under the `User` table as follows. The user's account and password are `user1:user1`.

```json
{
  "_id": {
    "$oid": "671249a93f1cf2f8bf9b2b82"
  },
  "api_keys": [
    {
      "_id": null,
      "revision_id": null,
      "api_key": "4d72c063-881f-45fa-85ab-3375c84f5dd7",
      "last_used": 0
    }
  ],
  "email": "user1@example.com",
  "password": "$2b$12$QFk6uHDBM5s69uSXrchivOC5SbpTUGV4tjmWz0nRvPSiMt.WAZVhC",
  "total_tokens": 0,
  "username": "user1",
  "callback_url": "http://127.0.0.1:9000/v1/callback/usage"
}
```

#### Business Backend

Create a user under the `User` table as follows. The user's account and password are `client1:client1`.

```json
{
  "_id": {
    "$oid": "671247fadb2faa4fec2c6f39"
  },
  "api_keys": [],
  "email": "client1@example.com",
  "password": "$2b$12$fWy.Yjs9x5zSRirRibjliO4GX66GSO/.GuG7he9lIatuiNDoPPb9a",
  "username": "client1"
}
```

### Environment Variables

#### LLM Server

```
SECRET_KEY // JWT secret key
ALGORITHM // JWT encryption algorithm
ACCESS_TOKEN_EXPIRE_MINUTES // JWT access token expiration time
REFRESH_TOKEN_EXPIRE_MINUTES // JWT refresh token expiration time
MONGODB_URL // MongoDB address
MONGODB_DB // MongoDB database name
ADMIN_USER_PASSWORD // Administrator password
OPENAI_BASE_URL // Wrapped OpenAI base URL
OPENAI_API_KEY // Wrapped OpenAI API key
```

#### Business Backend

LLM_USER_ID is the ID of the user registered by the business backend on the LLM server, and LLM_KEY is the key obtained by the user registered by the business backend on the LLM server.

```
SECRET_KEY // JWT secret key
ALGORITHM // JWT encryption algorithm
ACCESS_TOKEN_EXPIRE_MINUTES // JWT access token expiration time
REFRESH_TOKEN_EXPIRE_MINUTES // JWT refresh token expiration time
MONGODB_URL // MongoDB address
MONGODB_DB // MongoDB database name
ADMIN_USER_PASSWORD // Administrator password
LLM_KEY = "4d72c063-881f-45fa-85ab-3375c84f5dd7"
LLM_USER_ID = "671249a93f1cf2f8bf9b2b82"
```

### Interface Conventions

- `llm_server_url`: http://127.0.0.1:8000
- `backend_url`: http://127.0.0.1:9000

- `backend_url/user/login`: User login
  - **data**
    - username
    - password
  - **response**
    - access_token: Token needed for subsequent interaction with the business backend
    - refresh_token: Used to refresh the access token
    - token_type
- `backend/key/create`: Generate dynamic key
  - **header**
    - bearer
  - **response**
    - token: Dynamic key, used as the dynasealtoken request header when interacting with the LLM server
- `llm_server_url/client-side/chat/completions`: Request large model, this request will verify the client-side request, and inappropriate requests will throw errors
  - **header**
    - dynasealtoken
  - **body**
    Same as OpenAI format
  - **response**
    Same as OpenAI format
- `backend_url/callback/usage`: Callback interface, after the LLM server responds to the client-side request, the LLM server will send a request to inform the business backend of the content and token count of this request
  - event_id: Event ID of the dynamic key
  - content: Content of the large model response
  - tokens: Number of tokens consumed by the large model

## Starting the Project

1. Start the LLM server

```
cd llm-server
python main.py
```

2. Start the business backend

```
cd backend
python main.py
```

3. Run the client to check if the call is successful

```
cd client
python request_side.py
```

After successful operation, the client terminal can output streamingly, and the backend terminal will print `event_id`, `content`, and `tokens`.

Client terminal
![](https://cdn.studyinglover.com/pic/2024/10/708c69e378fb777d55fa159b378c8d2e.png)

Backend terminal
![](https://cdn.studyinglover.com/pic/2024/10/782aff898b90131833f310e75871f50c.png)

## Not Implemented

- [ ] Store callback requests in the database
- [ ] LLM server registration and backend registration
- [ ] ...
