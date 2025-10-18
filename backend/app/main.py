"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for managing Lorcana cards with OCR",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Lorcana Card Manager API",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker."""
    return {"status": "healthy", "service": "lorcana-card-manager"}


# Import routers will be added here
# from app.api import cards, images, ocr
# app.include_router(cards.router, prefix="/api/cards", tags=["cards"])
# app.include_router(images.router, prefix="/api/images", tags=["images"])
# app.include_router(ocr.router, prefix="/api/ocr", tags=["ocr"])
