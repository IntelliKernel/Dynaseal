import base64
import json
import os
from typing import Annotated, List

from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.global_model import Token, User, credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, key=os.environ["SECRET_KEY"], algorithms=os.environ["ALGORITHM"]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email


def decode_base64url(data):
    """将 Base64URL 解码成正常的字符串"""
    # Base64URL 是 Base64 的一种变种，"-" 替换为 "+", "_" 替换为 "/"
    data = data.replace("-", "+").replace("_", "/")
    # 修正可能缺少的 padding
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)
    return base64.b64decode(data)


async def get_dynaseal_token(Authorization: str = Header(None)):
    try:
        if not Authorization:
            raise credentials_exception

        # Authorization是bearer开头的，去掉bearer
        Authorization = Authorization[7:]

        # token格式为header.payload.signature，payload是{"api-key": id,"model": "deepseek-chat","max_token": 100,"expiring": time.time() + 15,}生成的，取出api-key
        header, payload, signature = Authorization.split(".")
        # base64解码payload
        # payload = {
        # "api-key": settings.llm_user_id,
        # "model": "deepseek-chat",
        # "max_tokens": 100,
        # "expiring": time.time() + 15,
        # "event_id": str(uuid.uuid4()),
        # }
        payload = json.loads(decode_base64url(payload))

        user_id = payload.get("api-key")
        user = await User.get(user_id)
        user_keys = [key.api_key for key in user.api_keys]
        for key in user_keys:
            # 用key验证token
            if jwt.decode(Authorization, key, algorithms=[os.environ["ALGORITHM"]]):
                return Token(
                    api_key=user_id,
                    model=payload.get("model"),
                    max_tokens=payload.get("max_tokens"),
                    expiring=payload.get("expiring"),
                    event_id=payload.get("event_id"),
                )
            else:
                continue

        return credentials_exception

    except Exception as e:
        print(e)
        raise credentials_exception


CurrentUser = Annotated[User, Depends(get_current_user)]
DynasealToken = Annotated[Token, Depends(get_dynaseal_token)]
