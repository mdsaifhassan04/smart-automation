import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.config import get_settings

class AuthService:
    def __init__(self):
        self.settings = get_settings()
        self.secret_key = self.settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 60 * 24 * 7 # 7 days
        
    async def generate_otp(self, phone: str) -> str:
        """Generate a 6-digit OTP."""
        if self.settings.ENABLE_MOCK_AUTH:
            return "123456"
        # In production, use a secure random generator and send via SMS API
        return "123456"
        
    async def verify_otp(self, phone: str, code: str) -> bool:
        """Verify OTP."""
        if self.settings.ENABLE_MOCK_AUTH:
            return code == "123456"
        return False
        
    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
        
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
