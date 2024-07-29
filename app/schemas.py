from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId  # Importar ObjectId

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


class TaskListBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskListCreate(TaskListBase):
    pass

class TaskList(TaskListBase):
    id: str
    owner_id: str

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str,
        }    


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    task_list_id: str

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str,
        }