from datetime import datetime

import uvicorn
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str
    root_path: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

db_client = AsyncIOMotorClient(settings.mongo_uri)
db = db_client.todoDb

description = """
API with stack: 
* fastapi
* mongo
* poetry
* docker
* kubernetes
"""
app = FastAPI(
    title="Тестовый проект",
    description=description,
    version="1.0.0",
    docs_url="/",
    root_path=settings.root_path,
)

MONGO_ID_REGEX = r"^[a-f\d]{24}$"


class Todo(BaseModel):
    title: str
    completed: bool = False


class TodoId(BaseModel):
    id: str


class TodoRecord(TodoId, Todo):
    created_date: datetime
    updated_date: datetime


class NotFoundException(BaseModel):
    detail: str = "Not Found"


@app.post("/todos", response_model=TodoId)
async def create_todo(payload: Todo) -> TodoId:
    """
    Create a new Todo
    """
    now = datetime.utcnow()
    insert_result = await db.todos.insert_one(
        {
            "title": payload.title,
            "completed": payload.completed,
            "created_date": now,
            "updated_date": now,
        }
    )

    return TodoId(id=str(insert_result.inserted_id))


@app.get(
    "/todos/{id}",
    response_model=TodoRecord,
    responses={
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def get_todo(
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX)
) -> TodoRecord:
    """
    Get a Todo
    """
    doc = await db.todos.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Not Found")

    return TodoRecord(
        id=str(doc["_id"]),
        title=doc["title"],
        completed=doc["completed"],
        created_date=doc["created_date"],
        updated_date=doc["updated_date"],
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


@app.put(
    "/todos/{id}",
    response_model=TodoId,
    responses={
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def update_todo(
    payload: Todo,
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX),
) -> TodoId:
    """
    Update a Todo
    """
    now = datetime.utcnow()
    update_result = await db.todos.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "title": payload.title,
                "completed": payload.completed,
                "updated_date": now,
            }
        },
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    return TodoId(id=id)


@app.delete(
    "/todos/{id}",
    response_model=bool,
    responses={
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def delete_todo(
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX),
) -> bool:
    """
    Delete a Todo
    """
    delete_result = await db.todos.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    return True


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
