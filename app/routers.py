from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List
from .schemas import UserCreate, UserResponse, Token, TaskListCreate, TaskList, Task, TaskCreate
from .crud import create_task, create_user, delete_task, delete_task_list, get_task, get_tasks, get_users, create_task_list as create_task_list_crud, get_task_lists, get_task_list, update_task, update_task_list
from .crud import TaskCreate, Task
from .auth import authenticate_user, create_access_token, get_current_user
from .database import get_database

user_router = APIRouter()
task_list_router = APIRouter()
task_router = APIRouter()



#---------------- Routers de Tasks --------------------------#

@user_router.post("/", response_model=UserResponse)
async def register_user(user: UserCreate):
    database = await get_database()
    existing_user = await database["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = await create_user(user)
    return new_user

@user_router.get("/", response_model=List[UserResponse])
async def read_users():
    users = await get_users()
    return users

@user_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@task_list_router.post("/task_lists/", response_model=TaskList)
async def create_task_list_endpoint(task_list: TaskListCreate, current_user: dict = Depends(get_current_user)):
    if "id" not in current_user:
        raise HTTPException(status_code=400, detail="User ID not found")
    print('Valor de id: ' + current_user["id"])
    return await create_task_list_crud(task_list=task_list, user_id=current_user["id"])

@task_list_router.get("/task_lists/", response_model=List[TaskList])
async def read_task_lists(skip: int = 0, limit: int = 10):
    return await get_task_lists(skip=skip, limit=limit)

@task_list_router.get("/task_lists/{task_list_id}", response_model=TaskList)
async def read_task_list(task_list_id: str):
    task_list = await get_task_list(task_list_id)
    if task_list is None:
        raise HTTPException(status_code=404, detail="Task list not found")
    return task_list


@task_list_router.put("/task_lists/{task_list_id}", response_model=TaskList)
async def update_task_list_endpoint(task_list_id: str, task_list: TaskListCreate):
    updated_task_list = await update_task_list(task_list_id, task_list)
    if updated_task_list is None:
        raise HTTPException(status_code=404, detail="Task list not found")
    return updated_task_list

@task_list_router.delete("/task_lists/{task_list_id}", response_model=dict)
async def delete_task_list_endpoint(task_list_id: str):
    deleted = await delete_task_list(task_list_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task list not found")
    return {"message": "Task list deleted successfully"}

#---------------- Routers de Tasks --------------------------#

@task_router.post("/tasks/", response_model=Task)
async def create_task_endpoint(task: TaskCreate, task_list_id: str, current_user: dict = Depends(get_current_user)):
    if "id" not in current_user:
        raise HTTPException(status_code=400, detail="User ID not found")
    return await create_task(task=task, task_list_id=task_list_id)

@task_router.get("/tasks/", response_model=List[Task])
async def read_tasks(task_list_id: str, skip: int = 0, limit: int = 10):
    return await get_tasks(task_list_id=task_list_id, skip=skip, limit=limit)

@task_router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: str):
    task = await get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@task_router.put("/tasks/{task_id}", response_model=Task)
async def update_task_endpoint(task_id: str, task: TaskCreate):
    updated_task = await update_task(task_id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@task_router.delete("/tasks/{task_id}")
async def delete_task_endpoint(task_id: str):
    success = await delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}