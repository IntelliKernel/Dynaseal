import time
from src.global_dependency import DynasealToken
from fastapi import HTTPException
from src.chat.model import ChatRequest

import asyncio
from datetime import datetime
import json
from beanie import PydanticObjectId
from fastapi.responses import StreamingResponse
from src.global_model import User
from src.chat.model import ChatRequest, Message, OPENAI_ASYNC_CLIENT
from src.client_side.model import GetUsageReq
from src.http import session
from src.global_dependency import DynasealToken
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai import AsyncStream


async def req_chat_completions(req: ChatRequest, token: DynasealToken):

    async def request_callback(user: User, token: DynasealToken, content, tokens):
        async with session().post(
            user.callback_url,
            json={
                "event_id": token.event_id,
                "content": content,
                "tokens": tokens,
            },
        ) as resp:
            pass

    async def event_generator(response: AsyncStream[ChatCompletionChunk], user: User):
        content: str = ""
        tokens: int = 0
        async for chunk in response:
            content += (
                chunk.choices[0].delta.content
                if chunk.choices[0].delta.content is not None
                else ""
            )
            tokens += chunk.usage.total_tokens if chunk.usage else 0
            yield f"data: {json.dumps(chunk.model_dump())}\n\n"
        asyncio.create_task(request_callback(user, token, content, tokens))

    user = await User.get(token.api_key)
    if req.stream:
        response = await OPENAI_ASYNC_CLIENT().chat.completions.create(
            model=req.model, messages=req.messages, stream=req.stream
        )

        return StreamingResponse(
            event_generator(response, user), media_type="text/event-stream"
        )
    else:
        response = await OPENAI_ASYNC_CLIENT().chat.completions.create(
            model=req.model, messages=req.messages, stream=req.stream
        )
        return response


async def process_req(req: ChatRequest, token: DynasealToken):
    if time.time() > int(token.expiring):
        raise HTTPException(
            status_code=400,
            detail="Token expired",
        )

    if req.max_tokens and req.max_tokens > token.max_tokens:
        raise HTTPException(
            status_code=400,
            detail="Max tokens exceeds token limit",
        )
    if req.model != token.model:
        raise HTTPException(
            status_code=400,
            detail="Model mismatch",
        )
