import os
import uuid
from fastapi import UploadFile, HTTPException
import logging

logger = logging.getLogger(__name__)

# Allowed audio extensions
ALLOWED_EXTENSIONS = {
    '.mp3', '.wav', '.m4a', '.mp4', '.webm', '.ogg', 
    '.flac', '.aac', '.wma', '.opus'
}

# Allowed MIME types
ALLOWED_MIME_TYPES = {
    'audio/wav', 'audio/x-wav', 'audio/wave',
    'audio/mpeg', 'audio/mp3', 'audio/mp4',
    'audio/x-m4a', 'audio/webm', 'audio/ogg',
    'audio/flac', 'audio/aac'
}

async def save_upload_file(upload_file: UploadFile, upload_dir: str) -> str:
    """
    Save uploaded audio file and return the file path
    """
    # Get file extension from filename
    original_filename = upload_file.filename
    if not original_filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    file_ext = os.path.splitext(original_filename)[1].lower()
    
    # Get MIME type
    mime_type = upload_file.content_type.lower() if upload_file.content_type else ""
    
    logger.info(f"File: {original_filename}")
    logger.info(f"Extension: {file_ext}")
    logger.info(f"MIME type: {mime_type}")
    
    # Validate by extension or MIME type
    if file_ext not in ALLOWED_EXTENSIONS and mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Extension: {file_ext}, MIME: {mime_type}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    content = await upload_file.read()
    
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    logger.info(f"File saved to: {file_path}, size: {len(content)} bytes")
    
    return file_path

def cleanup_file(file_path: str):
    """
    Remove temporary audio file
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up: {file_path}")
    except Exception as e:
        logger.error(f"Error cleaning up file {file_path}: {e}")