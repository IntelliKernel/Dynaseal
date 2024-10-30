from typing import Any
from beanie import PydanticObjectId
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    WebSocket,
    WebSocketDisconnect,
)
from src.global_dependency import DynasealToken
from src.chat.model import ChatRequest, Message, OPENAI_ASYNC_CLIENT
from src.chat.logic import req_chat_completions, process_req

router = APIRouter(tags=["ClientSideChat"], prefix="/chat")


@router.post("/completions")
async def chat(req: ChatRequest, token: DynasealToken):
    await process_req(req, token)
    return await req_chat_completions(req, token)
