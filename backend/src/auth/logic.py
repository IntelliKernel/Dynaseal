from datetime import datetime, timedelta
from jose import jwt
import os
from jose import JWTError, jwt 
from passlib.hash import bcrypt

from src.global_model import credentials_exception
from src.global_model import User

def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


def get_password_hash(password):
    return bcrypt.hash(password)

async def validate_user(email: str, password: str) -> bool:
    # 从数据库中验证用户
    user = await User.find_one({"email": email})
    if user is None:
        return False
    if not verify_password(password, user.password):
        return False
        
    return True

# 生成access_token和refresh_token，两个过期时间不同
async def create_tokens(data: dict, access_token_expires: int, refresh_token_expires: int) -> tuple:
    access_token_expires = timedelta(minutes=int(access_token_expires))
    refresh_token_expires = timedelta(minutes=int(refresh_token_expires))
    access_token = create_access_token(data, access_token_expires)
    refresh_token = create_access_token(data, refresh_token_expires)
    return access_token, refresh_token

# 生成token
def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"])
    return encoded_jwt

# 验证刷新token的请求
def validate_refresh_token(refresh_token: str) -> dict:
    try:
        payload = jwt.decode(refresh_token, os.environ["SECRET_KEY"], algorithms=os.environ["ALGORITHM"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return payload



async def create_test_user(username: str, email: str, password: str):
    user = User(username=username, email=email, password=get_password_hash(password))
    await user.save()
    
async def register_user(username: str, email: str, password: str):
    user = User(username=username, email=email, password=get_password_hash(password))
    await user.save()
    return user