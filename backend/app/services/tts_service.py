from gtts import gTTS
import os
import uuid

class TTSService:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "static", "audio")
        os.makedirs(self.output_dir, exist_ok=True)
        
    async def generate_audio(self, text: str, language: str = "hi") -> str:
        """Generate audio from text using gTTS and return file path."""
        # Note: gTTS supports 'hi' for Hindi, 'bn' for Bengali, etc.
        # Fallback to Hindi if not natively supported by gTTS (e.g. Bhojpuri)
        supported_langs = ['hi', 'en', 'bn', 'gu', 'kn', 'ml', 'mr', 'ta', 'te', 'ur']
        if language not in supported_langs:
            language = "hi"
            
        tts = gTTS(text=text, lang=language, slow=False)
        filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
        file_path = os.path.join(self.output_dir, filename)
        
        tts.save(file_path)
        return filename
