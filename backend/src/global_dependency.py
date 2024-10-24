import os
from typing import Annotated, List

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt 

from src.global_model import User, credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, key=os.environ["SECRET_KEY"], algorithms=os.environ["ALGORITHM"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email

CurrentUser = Annotated[User, Depends(get_current_user)]