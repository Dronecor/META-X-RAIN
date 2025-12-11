from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid
from backend.config import settings

router = APIRouter()

UPLOAD_DIR = "backend/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Return URL (assuming localhost or configured domain)
        # For demo, we return a relative path or full URL if we knew the host.
        # Let's return a relative path that can be served.
        # Base URL should be handled by the client or configured.
        
        return {"url": f"/static/uploads/{filename}", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
