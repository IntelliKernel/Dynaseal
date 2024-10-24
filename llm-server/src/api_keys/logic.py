from datetime import datetime
import json
import uuid
from beanie import PydanticObjectId
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from src.global_model import APIKey, User
from src.global_dependency import CurrentUser
from src.api_keys.model import GetAllKeysRequest, GetAllKeysResponse


async def _get_all_keys(req: GetAllKeysRequest):
    user = await User.get(req.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return GetAllKeysResponse(
        keys=[f"{key.api_key}.{user.id}" for key in user.api_keys]
    )


async def _create_api_key(user_email: CurrentUser):
    user = await User.find_one(User.email == user_email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    api_key = APIKey(api_key=str(uuid.uuid4()))
    user.api_keys.append(api_key)
    await user.save()
    return api_key
