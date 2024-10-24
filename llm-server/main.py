from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import uvicorn

import os
import importlib.util
from contextlib import asynccontextmanager
from src.http import close_session

from src.database import app_init


async def startup():
    await app_init()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()

    yield

    await close_session()


app = FastAPI(lifespan=lifespan, root_path="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


def load_routers_from_src():
    def load_routers_from_dir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isdir(file_path):
                load_routers_from_dir(file_path)
            elif filename.endswith(".py"):
                module_name = filename[:-3]  # remove '.py' extension
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "router"):
                    app.include_router(module.router, prefix="/v1")

    src_dir = os.path.join(os.path.dirname(__file__), "src")
    load_routers_from_dir(src_dir)


load_dotenv()
load_routers_from_src()
if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
