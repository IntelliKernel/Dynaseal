import asyncio
from datetime import datetime
import json
from beanie import PydanticObjectId
from fastapi.responses import StreamingResponse
from src.global_model import User
from src.chat.model import ChatRequest, Message, OPENAI_ASYNC_CLIENT
from src.http import session
from src.global_dependency import DynasealToken
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai import AsyncStream


async def req_chat_completions(req: ChatRequest, token: DynasealToken):

    async def event_generator(response: AsyncStream[ChatCompletionChunk]):
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

    user = await User.get(token.api_key)
    if req.stream:
        response = await OPENAI_ASYNC_CLIENT().chat.completions.create(
            model=req.model, messages=req.messages, stream=req.stream
        )

        return StreamingResponse(
            event_generator(response), media_type="text/event-stream"
        )
    else:
        response = await OPENAI_ASYNC_CLIENT().chat.completions.create(
            model=req.model, messages=req.messages, stream=req.stream
        )
        return response
