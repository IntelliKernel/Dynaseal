from motor.motor_asyncio import AsyncIOMotorClient
import glob
import inspect
import os
from importlib import import_module
from typing import Dict
import requests
import motor.motor_asyncio
from beanie import Document, PydanticObjectId, init_beanie
from src.global_model import User
from src.auth.logic import get_password_hash
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_server_url: str = "http://localhost:8000"


setting = Settings()


def get_db_models() -> list:
    obj_list = []
    src_path = os.path.dirname(__file__)
    idx_app_root = len(src_path.split(os.sep)) - 1
    for file in glob.glob(os.path.join(src_path, "**/*model.py"), recursive=True):
        mod = ".".join(file.split(os.sep)[idx_app_root:])[:-3]
        module = import_module(mod)
        classes = inspect.getmembers(module, inspect.isclass)
        obj_list += [
            o for (_, o) in classes if issubclass(o, Document) and o not in obj_list
        ]  # _ is the name of the class

    obj_str_list = [f"{o.__module__}.{o.__name__}" for o in obj_list]
    return obj_str_list  # or obj_list, both works


def _get_db_client():
    return motor.motor_asyncio.AsyncIOMotorClient(
        os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
    )  # 这个函数不是纯的, 每次都会重新开启一个 client


def _get_db_name():
    return os.environ.get("MONGODB_DB", "test")


async def init_admin():
    admin_email = "admin@dynaseal.backend.studyinglover.top"
    admin_password = os.environ.get("ADMIN_USER_PASSWORD", "admin")
    admin = await User.find_one(User.email == admin_email)
    if not admin:
        admin = User(
            username="admin",
            email=admin_email,
            password=get_password_hash(admin_password),
            llm_server_id="671223c5ca63f3d5f5275636",
            api_keys=[],
        )
    admin.password = get_password_hash(admin_password)
    await admin.save()


async def app_init():
    # 初始化数据库连接
    client = _get_db_client()
    database = _get_db_name()
    await init_beanie(database=client[database], document_models=get_db_models())
    await init_admin()
