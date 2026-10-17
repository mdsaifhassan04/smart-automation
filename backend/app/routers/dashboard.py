from fastapi import APIRouter
from app.models.schemas import DashboardStatsResponse

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats():
    """Return impact statistics matching the SIH 2026 presentation data."""
    return {
        "success_rates": [
            {"method": "Self-Serve Web Portals", "rate": 15, "color": "#9ca3af"},
            {"method": "Cyber Café (Intermediary)", "rate": 35, "color": "#f59e0b"},
            {"method": "Info-Only Mobile Apps", "rate": 40, "color": "#3b82f6"},
            {"method": "Gaon Ka Form", "rate": 95, "color": "#16a34a"}
        ],
        "impact_stats": [
            {
                "label": "Target Users",
                "value": "1.13 Cr+",
                "icon": "👥",
                "description": "Marginalized farmers in Bihar excluded from PM-KISAN due to registration errors"
            },
            {
                "label": "Funds Unlocked",
                "value": "₹50 Cr+",
                "icon": "💰",
                "description": "Unutilized PM-KISAN funds recoverable by fixing form errors"
            },
            {
                "label": "Informal Tax Eliminated",
                "value": "₹200-₹500",
                "icon": "🚫",
                "description": "Per-application charge by rural cyber café intermediaries"
            }
        ],
        "empowerment_cards": [
            {
                "title": "Direct Economic Relief",
                "description": "Eliminates the ₹200–₹500 informal 'tax' charged by rural intermediaries, saving crores annually for marginal farming families.",
                "icon": "💰"
            },
            {
                "title": "Maximized Fund Utilization",
                "description": "Reduces application rejections from 65% to <5% via strict AI-driven field validation before submission, ensuring government funds reach intended beneficiaries.",
                "icon": "✅"
            },
            {
                "title": "True Digital Inclusion",
                "description": "Shifts the paradigm from 'screen-first' to 'voice-first,' enabling illiterate citizens to navigate bureaucracy independently without intermediaries.",
                "icon": "🗣️"
            }
        ],
        "validation_data": [
            {
                "source": "CAG Audit Report (2022)",
                "stat": "1.13 Crore farmers excluded",
                "description": "Over 1.13 crore eligible farmers in Bihar were excluded from PM-KISAN due strictly to registration errors."
            },
            {
                "source": "Government Fiscal Data",
                "stat": "₹50.48 Crore failed DBT",
                "description": "Over ₹50.48 Crore in failed Direct Benefit Transfer payments directly attributed to mismatched applicant details and manual form errors."
            },
            {
                "source": "Primary Field Research",
                "stat": "23 days + ₹250 per application",
                "description": "Rural citizens spend an average of 23 days and ₹250 to successfully file a single 'free' government application."
            },
            {
                "source": "Cyber Café Study",
                "stat": "65% rejection rate",
                "description": "Cyber café intermediaries suffer a 65% rejection rate due to manual data-entry errors."
            }
        ],
        "total_applications": 12500,
        "applications_approved": 11875,
        "applications_pending": 625,
        "amount_disbursed": 71250000.0,
        "farmers_reached": 15000
    }
