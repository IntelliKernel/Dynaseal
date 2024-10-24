from datetime import timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import src.auth.logic as logic
import src.auth.model as model
from src.global_dependency import get_current_user, CurrentUser

router = APIRouter(tags=["Mail"], prefix="/mail")

@router.post("/send")
async def send_mail():
    return {"message": "Mail sent successfully"}