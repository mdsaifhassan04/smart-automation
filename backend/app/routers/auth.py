from fastapi import APIRouter, HTTPException
from app.models.schemas import OTPSendRequest, OTPSendResponse, OTPVerifyRequest, OTPVerifyResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])
auth_service = AuthService()

@router.post("/send-otp", response_model=OTPSendResponse)
async def send_otp(req: OTPSendRequest):
    """Send OTP to phone."""
    try:
        # Generate and store OTP in db (mocked in service)
        await auth_service.generate_otp(req.phone)
        return {"message": "OTP sent successfully", "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify-otp", response_model=OTPVerifyResponse)
async def verify_otp(req: OTPVerifyRequest):
    """Verify OTP and return JWT token."""
    try:
        is_valid = await auth_service.verify_otp(req.phone, req.code)
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid OTP")
            
        token = auth_service.create_token({"sub": req.phone})
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
