from fastapi import APIRouter, HTTPException
from app.models.schemas import IntentRequest, IntentResponse
from app.services.llm_service import LLMService

router = APIRouter(prefix="/api/v1/intent", tags=["Intent"])
llm_service = LLMService()

@router.post("/extract", response_model=IntentResponse)
async def extract_intent(req: IntentRequest):
    """Extract structured form fields from transcript."""
    try:
        result = await llm_service.extract_intent(req.transcript, req.existing_fields)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
