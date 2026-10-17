from fastapi import APIRouter, HTTPException
from app.models.schemas import EligibilityRequest, EligibilityResponse
from app.services.rag_service import RAGService

router = APIRouter(prefix="/api/v1/eligibility", tags=["Eligibility"])
rag_service = RAGService()

@router.post("/check", response_model=EligibilityResponse)
async def check_eligibility(req: EligibilityRequest):
    """Check scheme eligibility using RAG rules and LLM."""
    try:
        # Convert pydantic model to dict, excluding None values
        fields_dict = req.fields.model_dump(exclude_none=True)
        result = await rag_service.evaluate_eligibility(fields_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
