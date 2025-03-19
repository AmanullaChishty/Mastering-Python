# Custom dependencies include authentication and logging
from fastapi import Header, HTTPException, Request
from functools import wraps
from app.config import settings

def verify_token(auth:str=Header(...)):
    if auth != f"Bearer {settings.SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
def log_request(func):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        print(f"[LOG] Calling endpoint: {func.__name__}")
        result = await func(*args,**kwargs)
        print(f"[LOG] Finished endpoint: {func.__name__}")
        return result
    return wrapper