#This module simulates asynchronous task processing. It shows the use of async functions and background processing.
import asyncio
from typing import Dict

# In-memory task storage for demonstration purposes
TASK_DB = Dict[int, Dict] = {}

# process_task simulates a long-running task, updating progress every 0.5 seconds.
async def process_task(task):
    # Mark the task as "in progress"
    TASK_DB[task.task_id] = {"status": "in progress", "progress": 0.0, "result": ""}
    # Simulate a time-consuming task by updating progress incrementally
    for i in range(1,11):
        await asyncio.sleep(0.5)
        TASK_DB[task.task_id]['progress']=i*10 #update progress in %
    # Final result after processing
    TASK_DB[task.task_id]["status"]="completed"
    TASK_DB[task.task_id]["result"]=f"Processed data: {task.data}"
    return TASK_DB[task.task_id]["result"]

#get_task_status retrieves the current status of a given task.
async def get_tast_status(task_id: int):
    task = TASK_DB.get(task_id)
    if task:
        return task
    return {"status":"not found","progress":0.0,"result":""}