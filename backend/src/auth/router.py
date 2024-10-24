from datetime import timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import src.auth.logic as logic
import src.auth.model as model
from src.global_dependency import get_current_user, CurrentUser

router = APIRouter(tags=["User"], prefix="/user")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if not (await logic.validate_user(username, password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token, refresh_token = await logic.create_tokens(
        data={"sub": username}, access_token_expires=os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"], refresh_token_expires=os.environ["REFRESH_TOKEN_EXPIRE_MINUTES"]
    )
    token_model = model.Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    return token_model

@router.post("/refresh")
async def refresh(refresh_token: str, user: CurrentUser):
    username = logic.validate_refresh_token(refresh_token)
    access_token, refresh_token = await logic.create_tokens(
        data={"sub": username}, access_token_expires=os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"], refresh_token_expires=os.environ["REFRESH_TOKEN_EXPIRE_MINUTES"]
    )
    token_model = model.Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    return token_model
    

@router.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}

@router.post("/test/create")
async def create_test_user(username: str, email: str, password: str):
    await logic.create_test_user(username, email, password)
    return {"message": "User created successfully"}
