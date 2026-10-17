from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TranscribeRequest(BaseModel):
    # This will typically be form-data, but for symmetry we can have a model
    pass

class TranscribeResponse(BaseModel):
    text: str
    language: str
    confidence: float

class IntentRequest(BaseModel):
    transcript: str
    existing_fields: Optional[Dict[str, Any]] = None

class IntentResponse(BaseModel):
    fields: Dict[str, Any]
    is_correction: bool
    confidence: float

class FormField(BaseModel):
    farmer_name: Optional[str] = None
    father_husband_name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    category: Optional[str] = None
    farmer_type: Optional[str] = None
    aadhaar_number: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    sub_district: Optional[str] = None
    block: Optional[str] = None
    village: Optional[str] = None
    pincode: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    land_khata_number: Optional[str] = None
    khasra_dag_number: Optional[str] = None
    land_area_hectares: Optional[float] = None
    land_ownership_type: Optional[str] = None

class EligibilityRequest(BaseModel):
    fields: FormField

class EligibilityResponse(BaseModel):
    eligible: bool
    reasons: List[str]
    missing_fields: List[str]
    explanation: str

class FormGenerateRequest(BaseModel):
    fields: FormField
    scheme_name: str = "pm_kisan"

class FormGenerateResponse(BaseModel):
    download_url: str
    filename: str

class OTPSendRequest(BaseModel):
    phone: str

class OTPSendResponse(BaseModel):
    message: str
    success: bool

class OTPVerifyRequest(BaseModel):
    phone: str
    code: str

class OTPVerifyResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SuccessRateItem(BaseModel):
    method: str
    rate: int
    color: str

class ImpactStat(BaseModel):
    label: str
    value: str
    icon: str
    description: str

class EmpowermentCard(BaseModel):
    title: str
    description: str
    icon: str

class ValidationStat(BaseModel):
    source: str
    stat: str
    description: str

class DashboardStatsResponse(BaseModel):
    success_rates: List[SuccessRateItem]
    impact_stats: List[ImpactStat]
    empowerment_cards: List[EmpowermentCard]
    validation_data: List[ValidationStat]
    total_applications: int
    applications_approved: int
    applications_pending: int
    amount_disbursed: float
    farmers_reached: int

class TTSRequest(BaseModel):
    text: str
    language: str = "hi"

class ErrorResponse(BaseModel):
    detail: str
