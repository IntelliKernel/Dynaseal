from time import sleep
from fastapi import APIRouter
from src.callback.model import GetUsageReq

router = APIRouter(tags=["CallBack"], prefix="/callback")


@router.post("/usage")
async def get_usage(req: GetUsageReq):
    print(
        f"Get callback, enent_id: {req.event_id}, content: {req.content}, tokens: {req.tokens}"
    )
    sleep(10)
    return {"message": "success"}
