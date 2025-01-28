from fastapi import FastAPI, HTTPException, Depends, Request, APIRouter
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API Key from environment variables
API_KEY = os.getenv("LAB4_API_KEY")
if not API_KEY:
    raise RuntimeError("API key not found in environment variables")

# Initialize the FastAPI app
app = FastAPI()

# Sample data to represent Laboratories (TO-DO-LIST)
task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 1", "is_finished": False},
    {"task_id": 2, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False},
    {"task_id": 3, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 3", "is_finished": False},
]

# Task model for data validation
class Task(BaseModel):
    task_id: int
    task_title: str
    task_desc: str
    is_finished: bool

# API Key Authentication (Header-based or Query Parameter)
def verify_api_key(request: Request):
    # Check API key in headers
    api_key_header = request.headers.get("x-api-key")
    # Check API key in query parameters
    api_key_query = request.query_params.get("LAB4_API_KEY")

    if api_key_header != API_KEY and api_key_query != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True

# Helper function to find task by task_id
def find_task_by_id(task_id: int):
    for task in task_db:
        if task["task_id"] == task_id:
            return task
    return None

# API Versioning with routers
apiv1_router = APIRouter()
apiv2_router = APIRouter()

@app.get("/")
def read_root():
return {"message": "Hello, Render!"}

# GET
@app.get("/tasks/{task_id}")
def read_tasks(task_number: Optional[int] = None):

    #If user input is a negative number
    if task_number is not None and task_number < 0:
        return {"INVALID INPUT":"The task number input must not be a negative number"}
    
    if task_number:        

        for u in task_db: 
            #if the user input was available at the task_db
            if u["task_id"] == task_number:
                return {"STATUS": "Okay", "result" : u}
        
        #If task_id is not in the task_db
        if task_number != u["task_id"]:
            return {"NOTICE": "Task cannot be found"}

    #If the user did not input a task number
    return {"ERROR": "Task number is not provided, please put a task number to display a task before executing"}


# POST
@app.post("/tasks")
def create_tasks(list: Task):
    #If the user input is empty
    if list.task_id == 0:
        return {"ERROR": "Task number is not provided, please put a task number to display a task before executing"}
    
    #If task_id already existing
    if any(u['task_id'] == list.task_id for u in task_db):
        return {"ERROR": "Task number already existing"}
    #If user input is a negative number
    if list.task_id is not None and list.task_id <= -0:
            return {"INVALID INPUT":"The task number input must not be a negative number"}


    #If new Data is successfully created
    task_db.append(dict(list))
    return {"Status": "Okay"}



# DELETE
@app.delete("/tasks/{task_id}")
def delete_tasks(task_number: Optional[int] = None):
    #If user input is a negative number
    if task_number is not None and task_number < 0:
        return {"INVALID INPUT":"The task number input must not be a negative number"}
    if task_number:

        for idx, u in enumerate(task_db):
            #if the user input was available at the task_db is successfully  deleted
            if u["task_id"] == task_number:
                task_db.remove(u)
                return {"Status": "Okay", "Task is successfully deleted": u}

        #If task_id is not in the task_db
        if task_number != u["task_id"]:
            return {"NOTICE": "Task cannot be found"}
    #If the user input is empty
    return {"ERROR": "Task number is not provided, please put a task number to delete a task before executing"}

# PATCH
@app.patch("/tasks/{task_id}")
def update_tasks(task_id: int, list: Task):


    if task_id:
        # Find user by task_id
        for idx, u in enumerate(task_db):
            #If all data has been updated in user input
            if u["task_id"] == task_id:
                task_db[idx]['task_id'] = list.task_id
                task_db[idx]['task_title'] = list.task_title
                task_db[idx]['task_desc'] = list.task_desc
                task_db[idx]['is_finished'] = list.is_finished

                return {"status": "ok", "updated_data": task_db[idx]}
            #If user input is a negative number
            if task_id is not None and task_id <= -0:
                return {"INVALID INPUT":"The task number input must not be a negative number"}
            

    # Return an error message if there is no user found
    return {"error": "User not found. Cannot update record"}

# Version 2 - GET (Requires Authentication)

@apiv2_router.get("/tasks", dependencies=[Depends(verify_api_key)])#after requesting a request method, need muna mag-input ng API key bago mabigay ng response 
def read_all_tasks_v2():
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")#If walang tasks na nahanap
    return {"STATUS": "Okay", "tasks": task_db} #After ng response, may ganitong status
    
@apiv2_router.get("/tasks/{task_id}", dependencies=[Depends(verify_api_key)])#after requesting a request method, need muna mag-input ng API key bago mabigay ng response 
def read_task_v2(task_id: int):
    if task_id < 0:
        raise HTTPException(status_code=400, detail="Task ID must not be negative")#If yung task id na in-input is negative number
    
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"STATUS": "Okay", "result": task}

# Version 2 - POST (Requires Authentication)
@apiv2_router.post("/tasks", dependencies=[Depends(verify_api_key)])#after requesting a request method, need muna mag-input ng API key bago mabigay ng response 
def create_task_v2(task: Task):
    if task.task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid Task ID")#If yung in-input na task id is invalid
    if any(t['task_id'] == task.task_id for t in task_db):
        raise HTTPException(status_code=400, detail="Task ID already exists")#If yung task id na na-create is existing na
    
    task_db.append(task.dict())
    return {"Status": "Task created successfully"}#If succesfull yung bagong na-create na task id.

# Version 2 - DELETE (Requires Authentication)
@apiv2_router.delete("/tasks/{task_id}", dependencies=[Depends(verify_api_key)])#after requesting a request method, need muna mag-input ng API key bago mabigay ng response 
def delete_task_v2(task_id: int):
    if task_id < 0:
        raise HTTPException(status_code=400, detail="Task ID must not be negative")
    
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_db.remove(task)
    return {"Status": "Task deleted successfully", "Deleted Task": task}#If succesfull yung bagong na-delete na task id.

# Version 2 - PATCH (Requires Authentication)
@apiv2_router.patch("/tasks/{task_id}", dependencies=[Depends(verify_api_key)])#after requesting a request method, need muna mag-input ng API key bago mabigay ng response 
def update_task_v2(task_id: int, updated_task: Task):
    if task_id < 0:
        raise HTTPException(status_code=400, detail="Task ID must not be negative")
    
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.update(updated_task.dict())
    return {"Status": "Task updated successfully", "Updated Task": task}#If succesfull yung bagong na-update na task id.

# Register Version 1 and Version 2 Routers
app.include_router(apiv1_router, prefix="/apiv1")
app.include_router(apiv2_router, prefix="/apiv2")

# Protected Route Example
@app.get("/protected-route", dependencies=[Depends(verify_api_key)])#after requesting a request method, need muna mag-input ng API key bago mabigay ng response 
async def protected():
    return {"message": "You have access to this protected route"}
