from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings # noqa: F401

app = FastAPI(
    title="Task Management System API",
    description="A simple task management system with user authentication and role-based access control",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Task Management System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}