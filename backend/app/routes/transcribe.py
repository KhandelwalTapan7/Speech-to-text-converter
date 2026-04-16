from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from ..utils.audio import save_upload_file, cleanup_file
from ..whisper_model import whisper_model
import os
import logging
import traceback

logger = logging.getLogger(__name__)
router = APIRouter()
UPLOAD_DIR = "uploads"

@router.post("/transcribe")
async def transcribe_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    language: str = None
):
    """
    Transcribe audio file to text
    Supports: English (en), Hindi (hi), and many other languages
    """
    file_path = None
    
    try:
        # Validate file
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        logger.info(f"Processing file: {file.filename}, language: {language}")
        logger.info(f"Content type: {file.content_type}")
        
        # Save uploaded file
        file_path = await save_upload_file(file, UPLOAD_DIR)
        logger.info(f"File saved to: {file_path}")
        
        # Check if file was saved
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Failed to save file")
        
        # Get file size
        file_size = os.path.getsize(file_path)
        logger.info(f"File size: {file_size} bytes")
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Transcribe
        text = whisper_model.transcribe(file_path, language=language)
        
        if not text:
            text = "No speech detected in the audio file."
        
        logger.info(f"Transcription successful, text length: {len(text)}")
        
        # Prepare response
        response_data = {
            "success": True,
            "text": text,
            "language": language or "auto-detected",
            "filename": file.filename
        }
        
        return JSONResponse(content=response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        error_trace = traceback.format_exc()
        logger.error(f"Transcription failed: {error_msg}")
        logger.error(f"Traceback: {error_trace}")
        
        # Provide helpful error messages
        if "ffmpeg" in error_msg.lower():
            raise HTTPException(
                status_code=500, 
                detail="FFmpeg error. Please ensure FFmpeg is properly installed."
            )
        else:
            raise HTTPException(status_code=500, detail=f"Transcription failed: {error_msg}")
    
    finally:
        # Clean up temporary file
        if file_path and os.path.exists(file_path):
            background_tasks.add_task(cleanup_file, file_path)

@router.post("/transcribe-hindi")
async def transcribe_hindi(file: UploadFile = File(...)):
    """
    Specifically transcribe Hindi audio
    """
    return await transcribe_audio(file, language="hi")

@router.post("/transcribe-english")
async def transcribe_english(file: UploadFile = File(...)):
    """
    Specifically transcribe English audio
    """
    return await transcribe_audio(file, language="en")