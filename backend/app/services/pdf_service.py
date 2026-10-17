import fitz  # PyMuPDF
import os
import uuid
from typing import Dict, Any

class PDFService:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "static", "forms")
        os.makedirs(self.output_dir, exist_ok=True)
        
    async def generate_pm_kisan_form(self, fields: Dict[str, Any]) -> str:
        """Generates a PM-KISAN application form PDF from scratch."""
        
        doc = fitz.open()
        page = doc.new_page(width=fitz.paper_size("A4")[0], height=fitz.paper_size("A4")[1])
        
        # Use built-in Helvetica font
        font_name = "helv"
        
        y_pos = 50
        
        # Header
        page.insert_text((200, y_pos), "PM-KISAN Samman Nidhi Application Form", fontsize=16, fontname=font_name, color=(0,0,0))
        y_pos += 30
        page.insert_text((250, y_pos), "Government of India", fontsize=12, fontname=font_name, color=(0,0,0))
        y_pos += 40
        
        # Helper for printing rows
        def print_row(label: str, value: Any, y: int):
            page.insert_text((50, y), f"{label}:", fontsize=11, fontname=font_name, color=(0,0,0))
            val_str = str(value) if value else "________________________"
            page.insert_text((250, y), val_str, fontsize=11, fontname=font_name, color=(0,0,1)) # blue color for filled values
            return y + 25

        y_pos = print_row("Farmer Name", fields.get("farmer_name"), y_pos)
        y_pos = print_row("Father/Husband Name", fields.get("father_husband_name"), y_pos)
        y_pos = print_row("Gender", fields.get("gender"), y_pos)
        y_pos = print_row("Date of Birth", fields.get("date_of_birth"), y_pos)
        y_pos = print_row("Category", fields.get("category"), y_pos)
        y_pos = print_row("Farmer Type", fields.get("farmer_type"), y_pos)
        y_pos = print_row("Aadhaar Number", fields.get("aadhaar_number"), y_pos)
        y_pos = print_row("Mobile Number", fields.get("mobile_number"), y_pos)
        y_pos += 10
        
        page.insert_text((50, y_pos), "Address Details", fontsize=12, fontname=font_name, color=(0,0,0))
        y_pos += 25
        y_pos = print_row("Address", fields.get("address"), y_pos)
        y_pos = print_row("Village", fields.get("village"), y_pos)
        y_pos = print_row("Block", fields.get("block"), y_pos)
        y_pos = print_row("Sub-District", fields.get("sub_district"), y_pos)
        y_pos = print_row("District", fields.get("district"), y_pos)
        y_pos = print_row("State", fields.get("state"), y_pos)
        y_pos = print_row("Pincode", fields.get("pincode"), y_pos)
        y_pos += 10

        page.insert_text((50, y_pos), "Bank Details", fontsize=12, fontname=font_name, color=(0,0,0))
        y_pos += 25
        y_pos = print_row("Bank Name", fields.get("bank_name"), y_pos)
        y_pos = print_row("Account Number", fields.get("account_number"), y_pos)
        y_pos = print_row("IFSC Code", fields.get("ifsc_code"), y_pos)
        y_pos += 10
        
        page.insert_text((50, y_pos), "Land Details", fontsize=12, fontname=font_name, color=(0,0,0))
        y_pos += 25
        y_pos = print_row("Khata Number", fields.get("land_khata_number"), y_pos)
        y_pos = print_row("Khasra Number", fields.get("khasra_dag_number"), y_pos)
        y_pos = print_row("Area (Hectares)", fields.get("land_area_hectares"), y_pos)
        y_pos = print_row("Ownership Type", fields.get("land_ownership_type"), y_pos)
        y_pos += 20
        
        # Declaration
        decl_text = "I declare that I am not covered under any exclusion criteria of PM-KISAN."
        page.insert_text((50, y_pos), decl_text, fontsize=10, fontname=font_name, color=(0,0,0))
        y_pos += 40
        page.insert_text((50, y_pos), "Signature/Thumb Impression: ____________________", fontsize=11, fontname=font_name, color=(0,0,0))
        page.insert_text((400, y_pos), "Date: ________________", fontsize=11, fontname=font_name, color=(0,0,0))
        
        filename = f"pm_kisan_{uuid.uuid4().hex[:8]}.pdf"
        file_path = os.path.join(self.output_dir, filename)
        doc.save(file_path)
        doc.close()
        
        return filename
