from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import the router directly
from app.routes.transcribe import router

app = FastAPI(title="Speech to Text API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if not exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Include routes
app.include_router(router, prefix="/api", tags=["transcribe"])

@app.get("/")
async def root():
    return {"message": "Speech to Text API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}