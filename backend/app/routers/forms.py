from fastapi import APIRouter, HTTPException
from app.models.schemas import FormGenerateRequest, FormGenerateResponse
from app.services.pdf_service import PDFService

router = APIRouter(prefix="/api/v1/forms", tags=["Forms"])
pdf_service = PDFService()

@router.post("/generate", response_model=FormGenerateResponse)
async def generate_form(req: FormGenerateRequest):
    """Generate PDF form from fields."""
    try:
        fields_dict = req.fields.model_dump()
        filename = await pdf_service.generate_pm_kisan_form(fields_dict)
        return {
            "download_url": f"/static/forms/{filename}",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
