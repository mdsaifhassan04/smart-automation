from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
from app.services.asr_service import ASRService
from app.services.tts_service import TTSService
from app.models.schemas import TTSRequest
from app.config import get_settings

router = APIRouter(prefix="/api/v1/voice", tags=["Voice"])
asr_service = ASRService()
tts_service = TTSService()
settings = get_settings()

@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """Transcribe audio file using Whisper."""
    # Check size if needed, simple read here
    audio_bytes = await audio.read()
    
    # Simple size check based on config
    size_mb = len(audio_bytes) / (1024 * 1024)
    if size_mb > settings.MAX_AUDIO_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"File too large. Max {settings.MAX_AUDIO_SIZE_MB}MB allowed.")
    
    try:
        result = await asr_service.transcribe(audio_bytes, audio.filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts")
async def text_to_speech(req: TTSRequest):
    """Generate audio from text."""
    try:
        filename = await tts_service.generate_audio(req.text, req.language)
        return {"audio_url": f"/static/audio/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
