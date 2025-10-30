from fastapi import FastAPI
from pydantic import BaseModel
from app.password_checker import PasswordStrengthChecker
import uvicorn

app = FastAPI(
    title="Password Strength Checker Service",
    description="Микросервис для проверки сложности паролей",
    version="1.0.0"
)

class PasswordRequest(BaseModel):
    password: str

class PasswordResponse(BaseModel):
    strength: str
    score: int
    feedback: list[str]
    length: int

@app.get("/")
async def root():
    return {"message": "Password Strength Checker Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/check", response_model=PasswordResponse)
async def check_password_strength(request: PasswordRequest):
    result = PasswordStrengthChecker.check_strength(request.password)
    return PasswordResponse(**result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)