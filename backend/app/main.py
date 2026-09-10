"""
FastAPI Main Application

Office Suite Backend API v7.2
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List

from .core.database import init_db, close_db, get_db
from .core.config import settings
from .services.minio_service import minio_service
from .services.cloudinary_service import cloudinary_service
from .services.box_storage_service import box_service
from .api.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    await init_db()
    print("Database initialized")
    
    yield
    
    # Shutdown
    await close_db()
    print("Database connections closed")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Office Suite Backend API - Multi-cloud storage orchestration",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "description": "Multi-cloud storage orchestration backend",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "backend",
        "version": settings.APP_VERSION,
    }


@app.get("/api/v1/storage/services")
async def list_storage_services():
    """List all configured storage services."""
    services = []
    
    # MinIO (always enabled)
    services.append({
        "name": "MinIO",
        "type": "local",
        "enabled": True,
        "purpose": "Primary hot storage",
    })
    
    # Cloudinary
    if settings.CLOUDINARY_ENABLED:
        services.append({
            "name": "Cloudinary",
            "type": "cloud",
            "enabled": True,
            "purpose": "Media processing (25GB free)",
        })
    
    # Box
    if settings.BOX_ENABLED:
        services.append({
            "name": "Box",
            "type": "cloud",
            "enabled": True,
            "purpose": "Enterprise documents (10GB free)",
        })
    
    # Other services would be added here as they're implemented
    
    return {
        "services": services,
        "count": len(services),
    }


@app.get("/api/v1/storage/stats")
async def get_storage_stats():
    """Get storage usage statistics across all services."""
    stats = {
        "services": {},
        "total_used_gb": 0,
        "total_available_gb": 0,
    }
    
    # MinIO stats
    try:
        minio_stats = await minio_service.get_storage_stats()
        if minio_stats["success"]:
            stats["services"]["minio"] = minio_stats
    except Exception as e:
        stats["services"]["minio"] = {"error": str(e)}
    
    # Cloudinary stats
    if settings.CLOUDINARY_ENABLED:
        try:
            cloudinary_stats = await cloudinary_service.get_storage_stats()
            if cloudinary_stats["success"]:
                stats["services"]["cloudinary"] = cloudinary_stats
                stats["total_used_gb"] += cloudinary_stats.get("used_gb", 0)
                stats["total_available_gb"] += cloudinary_stats.get("total_gb", 25)
        except Exception as e:
            stats["services"]["cloudinary"] = {"error": str(e)}
    
    # Box stats would be added here
    
    return stats


@app.post("/api/v1/upload")
async def upload_file():
    """
    Upload a file to the appropriate storage service.
    
    This is a placeholder - full implementation requires:
    - File upload handling with FastAPI UploadFile
    - Storage service selection logic
    - Database record creation
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="File upload endpoint not yet implemented",
    )


@app.get("/api/v1/files")
async def list_files():
    """
    List files from storage.
    
    This is a placeholder - full implementation requires:
    - Database query for file records
    - Pagination support
    - Filtering options
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="File listing endpoint not yet implemented",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
