from beanie import PydanticObjectId
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    WebSocket,
    WebSocketDisconnect,
)
from src.global_dependency import CurrentUser
from src.key.logic import _create_key

router = APIRouter(tags=["Key"], prefix="/key")


@router.post("/create")
async def create_key(user: CurrentUser):
    return await _create_key(user)
