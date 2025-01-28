from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Task(BaseModel):
    task_id: int
    task_title: str
    task_desc: str
    is_finished: bool


# Sample data to represent Laboratories
#TO-DO-LIST
task_db = [
{"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 1", "is_finished": False},
{"task_id": 2, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False},
{"task_id": 3, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 3", "is_finished": False}
]

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