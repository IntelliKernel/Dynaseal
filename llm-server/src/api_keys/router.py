from beanie import PydanticObjectId
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    WebSocket,
    WebSocketDisconnect,
)
from src.api_keys.logic import _get_all_keys, _create_api_key
from src.api_keys.model import GetAllKeysRequest, GetAllKeysResponse
from src.global_dependency import CurrentUser

router = APIRouter(tags=["APIKeys"], prefix="/api_key")


@router.post("/list")
async def get_api_keys(req: GetAllKeysRequest):
    return await _get_all_keys(req)


@router.post("/create")
async def create_api_key(user_email: CurrentUser):
    return await _create_api_key(user_email)
