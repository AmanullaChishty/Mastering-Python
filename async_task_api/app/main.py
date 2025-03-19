#This is the main FastAPI application file where endpoints are defined. It brings together all modules.
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.config import settings
from app.models import TaskRequest, TaskResponse, StatusResponse
from app.dependencies import verify_token, log_request
from app.tasks import process_task, get_tast_status
from utils import generate_numbers

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

@app.post("/tasks/", response_model=TaskResponse, dependencies=[Depends(verify_token)])
@log_request
async def create_task(task: TaskRequest):
    result = await process_task(task)
    return TaskResponse(task_id=task.task_id, status="completed", result=result)

@app.get("/tasks/{task_id}/status", response_model=StatusResponse, dependencies=[Depends(verify_token)])
async def task_status(task_id: int):
    status_data = await get_tast_status(task_id)
    if status_data['status']=="not found":
        raise HTTPException(status_code=404, detail="Task Not Found")
    return StatusResponse(task_id=task_id,status=status_data["status"],progress=status_data["progress"])

@app.get("/stream/", dependencies=[Depends(verify_token)])
async def stream_numbers():
    # Using async generator to stream response
    generator = generate_numbers()
    return StreamingResponse(generator, media_type="text/plain")

# • /tasks/: Accepts a task submission, processes it asynchronously, and returns a response.
# • /tasks/{task_id}/status: Returns the current status of a task.
# • /stream/: Streams numbers using an asynchronous generator.