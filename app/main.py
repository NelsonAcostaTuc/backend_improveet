# main.py

from fastapi import FastAPI
from .database import connect_to_mongo, close_mongo_connection
from .routers import user_router, task_list_router, task_router

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    print("MongoDB connected successfully")

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(task_list_router, tags=["task_lists"])
app.include_router(task_router, tags=["tasks"])  # Incluir el nuevo router
