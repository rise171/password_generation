from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from app.logger import ActivityLogger
import uvicorn

app = FastAPI(
    title="Activity Logger Service",
    description="Микросервис для логирования действий пользователей",
    version="1.0.0"
)

logger = ActivityLogger()

class LogRequest(BaseModel):
    user_id: int
    action: str
    service_name: Optional[str] = None
    details: Optional[Dict] = None

class LogResponse(BaseModel):
    status: str
    message: str

class ActivityResponse(BaseModel):
    timestamp: str
    user_id: int
    action: str
    service_name: Optional[str]
    details: Dict

@app.get("/")
async def root():
    return {"message": "Activity Logger Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/log", response_model=LogResponse)
async def log_activity(request: LogRequest):
    result = logger.log_activity(
        user_id=request.user_id,
        action=request.action,
        service_name=request.service_name,
        details=request.details
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return LogResponse(**result)

@app.get("/activities/user/{user_id}", response_model=List[ActivityResponse])
async def get_user_activities(user_id: int, limit: int = 20):
    activities = logger.get_user_activities(user_id, limit)
    return activities

@app.get("/activities/recent", response_model=List[ActivityResponse])
async def get_recent_activities(limit: int = 20):
    activities = logger.get_recent_activities(limit)
    return activities

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)