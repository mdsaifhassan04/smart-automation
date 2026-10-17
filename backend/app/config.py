from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = "sk-placeholder"
    SECRET_KEY: str = "hackathon-secret-key-2026"
    ENABLE_MOCK_AUTH: bool = True
    DATABASE_URL: str = "sqlite+aiosqlite:///./gaonkaform.db"
    FRONTEND_URL: str = "http://localhost:3000"
    WHISPER_MODEL: str = "whisper-1"
    LLM_MODEL: str = "gpt-4o-mini"
    MAX_AUDIO_SIZE_MB: int = 25

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
