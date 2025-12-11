from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.config import settings
from backend.database import engine, Base, get_db
# Import models to ensure tables are created
from backend import models
import os

# Create tables
print(f"Connecting to database with engine: {engine.url}")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS - Updated for Vercel deployment
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8501", # Streamlit default port
    "http://localhost:8000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:5000",
]

# Add Vercel URL if in production
vercel_url = os.getenv("VERCEL_URL")
if vercel_url:
    origins.extend([
        f"https://{vercel_url}",
        f"http://{vercel_url}",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if os.getenv("VERCEL_ENV") != "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "environment": os.getenv("VERCEL_ENV", "local"),
        "version": "1.0.0"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Check DB connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy", 
            "database": "connected",
            "environment": os.getenv("VERCEL_ENV", "local")
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database not reachable: {e}")

from backend.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Vercel serverless handler
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    # Mangum not installed, skip (for local development)
    pass
