from typing import Optional
from pydantic import BaseModel, EmailStr
from bson import ObjectId  # Importar ObjectId


class UserModel(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

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