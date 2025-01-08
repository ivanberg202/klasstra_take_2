from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from uuid import uuid4

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "uploads"  # Directory to store files (adjust as needed)
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles file uploads and returns the URL of the uploaded file.
    """
    try:
        # Generate a unique filename
        file_id = str(uuid4())
        extension = os.path.splitext(file.filename)[-1]
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{extension}")
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Return the file's public URL (adjust base URL as needed)
        base_url = "http://127.0.0.1:8000"  # Change this for production
        file_url = f"{base_url}/{UPLOAD_DIR}/{file_id}{extension}"
        return {"url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail="File upload failed") from e
