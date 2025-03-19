# Define Pydantic models for request and response validation.

from pydantic import BaseModel

# TaskRequest: Validates incoming data with required fields task_id (int) and data (str).
class TaskRequest(BaseModel):
    task_id: int
    data: str

# TaskResponse: Structures the response with fields task_id (int), status (str), and result (str).
class TaskResponse(BaseModel):
    task_id: int
    status: str
    result: str
    
# StatusResponse: Used for status queries, returning task_id (int), status (str), and progress (float).
class StatusResponse(BaseModel):
    task_id: int
    status: str
    progress: float 