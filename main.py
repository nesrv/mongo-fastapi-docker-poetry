from datetime import datetime

import motor.motor_asyncio
import uvicorn
from fastapi import FastAPI
from envparse import Env
from fastapi.routing import APIRoute
from pydantic import BaseModel
from starlette.requests import Request

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

db_client = AsyncIOMotorClient(settings.mongo_uri)
db = db_client.todoDb

env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/test_database")


class Todo(BaseModel):
    title: str
    completed: bool = False


class TodoId(BaseModel):
    id: str


class TodoRecord(TodoId, Todo):
    created_date: datetime
    updated_date: datetime


# Инициализация
app = FastAPI(
    title="Mongo+Fastapi+Poetry+Docker",
    description="тестовый проект",
    version="0.0.1"
)


@app.get("/todos", response_model=list[TodoRecord])
async def get_todos() -> list[TodoRecord]:
    """
    Get Todos
    """
    todos: list[TodoRecord] = []
    async for doc in db.todos.find():
        todos.append(
            TodoRecord(
                id=str(doc["_id"]),
                title=doc["title"],
                completed=doc["completed"],
                created_date=doc["created_date"],
                updated_date=doc["updated_date"],
            )
        )

    return todos


@app.post("/todos", response_model=TodoId)
async def create_todo(payload: Todo) -> TodoId:
    """
    Create a new Todo
    """
    now = datetime.now()
    insert_result = await db.todos.insert_one(
        {
            "title": payload.title,
            "completed": payload.completed,
            "created_date": now,
            "updated_date": now,
        }
    )

    return TodoId(id=str(insert_result.inserted_id))


@app.get("/ping")
async def ping() -> dict:
    return {"Success": True}


@app.get("/")
async def mainpage() -> str:
    return "YOU ARE ON THE MAIN PAGE"


@app.post("/create_record")
async def create_record(request: Request) -> dict:
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["test_database"]
    await mongo_client.records.insert_one({"sample": "record"})
    return {"Success": True}


@app.get("/get_records")
async def get_records(request: Request) -> list:
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["test_database"]
    cursor = mongo_client.records.find({})
    res = []
    for document in await cursor.to_list(length=100):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res


routes = [
    # APIRoute(path="/ping", endpoint=ping, methods=["GET"]),
    APIRoute(path="/", endpoint=mainpage, methods=["GET"]),
    APIRoute(path="/create_record", endpoint=create_record, methods=["POST"]),
    APIRoute(path="/get_records", endpoint=get_records, methods=["GET"]),
]

client = AsyncIOMotorClient(MONGODB_URL)
# app = FastAPI()
app.state.mongo_client = client
# app.include_router(APIRouter(routes=routes))

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
