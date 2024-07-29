from .database import get_database
from .schemas import UserCreate
from .schemas import TaskListCreate, TaskList, Task, TaskBase, TaskCreate
from bson import ObjectId
import motor.motor_asyncio

async def create_user(user: UserCreate):
    database = await get_database()
    user_dict = user.dict()
    user_dict["disabled"] = False
    result = await database["users"].insert_one(user_dict)
    return user_dict

async def get_users():
    database = await get_database()
    users_cursor = database["users"].find()
    users = await users_cursor.to_list(length=None)
    return users


async def create_task_list(task_list: TaskListCreate, user_id: str):
    db = await get_database()
    task_list_dict = task_list.dict()
    task_list_dict["owner_id"] = user_id
    result = await db.task_lists.insert_one(task_list_dict)
    task_list_dict["_id"] = str(result.inserted_id)
    task_list_dict["id"] = str(result.inserted_id)  # Asegúrate de que 'id' está presente
    return TaskList(**task_list_dict)

async def get_task_lists(skip: int = 0, limit: int = 10):
    db = await get_database()
    task_lists_cursor = db.task_lists.find().skip(skip).limit(limit)
    task_lists = await task_lists_cursor.to_list(length=limit)
    for task_list in task_lists:
        task_list["id"] = str(task_list.pop("_id"))
    return [TaskList(**task_list) for task_list in task_lists]

async def get_task_list(task_list_id: str):
    db = await get_database()
    task_list = await db.task_lists.find_one({"_id": ObjectId(task_list_id)})
    if task_list:
        task_list["id"] = str(task_list.pop("_id"))
        return TaskList(**task_list)
    return None

async def update_task_list(task_list_id: str, task_list: TaskListCreate):
    db = await get_database()
    task_list_dict = task_list.dict()
    result = await db.task_lists.update_one({"_id": ObjectId(task_list_id)}, {"$set": task_list_dict})
    if result.modified_count == 1:
        updated_task_list = await db.task_lists.find_one({"_id": ObjectId(task_list_id)})
        updated_task_list["id"] = str(updated_task_list.pop("_id"))
        return TaskList(**updated_task_list)
    return None

async def delete_task_list(task_list_id: str):
    db = await get_database()
    result = await db.task_lists.delete_one({"_id": ObjectId(task_list_id)})
    return result.deleted_count == 1

#---------------- CRUD DE Task List--------------------------#

async def create_task(task: TaskCreate, task_list_id: str):
    db = await get_database()
    task_dict = task.dict()
    task_dict["task_list_id"] = task_list_id
    result = await db.tasks.insert_one(task_dict)
    task_dict["_id"] = str(result.inserted_id)
    task_dict["id"] = str(result.inserted_id)  # Asegúrate de que 'id' está presente
    return Task(**task_dict)

async def get_tasks(task_list_id: str, skip: int = 0, limit: int = 10):
    db = await get_database()
    tasks_cursor = db.tasks.find({"task_list_id": task_list_id}).skip(skip).limit(limit)
    tasks = await tasks_cursor.to_list(length=limit)
    for task in tasks:
        task["id"] = str(task.pop("_id"))  # Convertir _id a id
    return [Task(**task) for task in tasks]

async def get_task(task_id: str):
    db = await get_database()
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    if task:
        task['id'] = str(task.pop('_id'))  # Convertir _id a id
        return Task(**task)
    return None

async def update_task(task_id: str, task: TaskCreate):
    db = await get_database()
    task_dict = task.dict()
    result = await db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": task_dict})
    if result.modified_count == 1:
        updated_task = await db.tasks.find_one({"_id": ObjectId(task_id)})
        updated_task["_id"] = str(updated_task["_id"])
        return Task(**updated_task)
    return None

async def delete_task(task_id: str):
    db = await get_database()
    result = await db.tasks.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count == 1