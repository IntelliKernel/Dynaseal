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
from src.chat.model import ChatRequest, Message, OPENAI_ASYNC_CLIENT
from src.chat.logic import req_chat_completions

router = APIRouter(tags=["Chat"], prefix="/chat")


@router.post("/completions")
async def chat(req: ChatRequest):
    return await req_chat_completions(req)
