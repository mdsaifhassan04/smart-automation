from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.models.database import create_tables
from app.routers import voice, intent, eligibility, forms, auth, dashboard
from app.config import get_settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create necessary static directories
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "static", "forms"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "static", "audio"), exist_ok=True)
    
    # Init DB
    await create_tables()
    
    yield
    
app = FastAPI(title="Gaon Ka Form API", lifespan=lifespan)
settings = get_settings()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "*"], # allowing all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")

# Include routers
app.include_router(voice.router)
app.include_router(intent.router)
app.include_router(eligibility.router)
app.include_router(forms.router)
app.include_router(auth.router)
app.include_router(dashboard.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Gaon Ka Form API is running"}
