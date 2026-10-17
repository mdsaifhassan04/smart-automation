import json
import openai
from app.config import get_settings

class LLMService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=get_settings().OPENAI_API_KEY)
        self.model = get_settings().LLM_MODEL
    
    async def extract_intent(self, transcript: str, existing_fields: dict = None) -> dict:
        """Extract PM-KISAN form fields from transcribed speech."""
        system_prompt = """You are an expert AI assistant that helps Indian farmers fill government scheme application forms.
You understand Hindi, Bhojpuri, and Maithili dialects.

Your task: Extract structured form field values from the farmer's spoken transcript.

The PM-KISAN form requires these fields:
- farmer_name: Full name of the farmer (as on Aadhaar)
- father_husband_name: Father's or Husband's name
- gender: Male/Female/Other (पुरुष/महिला/अन्य)
- date_of_birth: Date of birth (YYYY-MM-DD format)
- category: General/SC/ST/OBC
- farmer_type: Small & Marginal / Others
- aadhaar_number: 12-digit Aadhaar number (remove spaces)
- mobile_number: 10-digit mobile number
- address: Residential address
- state: State name
- district: District name
- sub_district: Sub-district/Tehsil
- block: Block name  
- village: Village name
- pincode: 6-digit PIN code
- bank_name: Bank name
- account_number: Bank account number
- ifsc_code: 11-character IFSC code
- land_khata_number: Khata/Khatoni number
- khasra_dag_number: Khasra/Dag/Plot number
- land_area_hectares: Land area in hectares (if given in acres, convert: 1 acre = 0.4047 hectares, if given in bigha, convert: 1 bigha ≈ 0.25 hectares)
- land_ownership_type: Single/Joint

Rules:
1. Extract ONLY the fields mentioned in the transcript. Don't fabricate values.
2. For numbers (Aadhaar, mobile, account), remove all spaces and format correctly.
3. Convert local units to standard: acres/bigha → hectares.
4. If the farmer says "do ekad" or "दो एकड़", convert to 0.8094 hectares.
5. Understand Bhojpuri/Maithili variants: "हमार" = "मेरा" (my), "बाबूजी" = "पिताजी" (father), "गाँव" = village
6. If the transcript is a correction (e.g., "my name is actually X not Y"), return only the corrected field.
7. Return ONLY a valid JSON object with the extracted fields. No explanation text.

Return format: {"fields": {"field_name": "value", ...}, "is_correction": false}"""

        user_prompt = f"Farmer's speech transcript: \"{transcript}\""
        if existing_fields:
            user_prompt += f"\n\nAlready captured fields: {json.dumps(existing_fields, ensure_ascii=False)}"
            user_prompt += "\nIf the transcript corrects any existing field, return is_correction: true and only the corrected fields."

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return {
            "fields": result.get("fields", {}),
            "is_correction": result.get("is_correction", False),
            "confidence": 0.9
        }
    
    async def translate_to_local(self, text: str, target_lang: str) -> str:
        """Translate text to local language for TTS readback."""
        lang_map = {"hi": "Hindi", "bho": "Bhojpuri", "mai": "Maithili", "en": "English"}
        lang_name = lang_map.get(target_lang, "Hindi")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"Translate the following text to {lang_name}. Return ONLY the translation, nothing else."},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
