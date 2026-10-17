import openai
import tempfile
import os
from app.config import get_settings

class ASRService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=get_settings().OPENAI_API_KEY)
        self.agri_prompt = (
            "किसान का नाम, आधार संख्या, मोबाइल नंबर, बैंक खाता, "
            "IFSC कोड, खसरा नंबर, खाता नंबर, जमीन, एकड़, हेक्टेयर, "
            "ग्राम, पंचायत, ब्लॉक, जिला, बिहार, पीएम किसान, "
            "प्रधानमंत्री किसान सम्मान निधि, राशन कार्ड।"
        )
    
    async def transcribe(self, audio_bytes: bytes, filename: str) -> dict:
        """Transcribe audio using Whisper API with Hindi language + agri context."""
        with tempfile.NamedTemporaryFile(suffix=self._get_extension(filename), delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        
        try:
            with open(tmp_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="hi",
                    prompt=self.agri_prompt,
                    response_format="verbose_json"
                )
            return {
                "text": transcript.text,
                "language": transcript.language or "hi",
                "confidence": 0.85  # Whisper API doesn't return confidence directly
            }
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def _get_extension(self, filename: str) -> str:
        if ".webm" in filename:
            return ".webm"
        elif ".mp4" in filename:
            return ".mp4"
        elif ".wav" in filename:
            return ".wav"
        return ".webm"
