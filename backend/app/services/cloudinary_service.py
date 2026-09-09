"""
Cloudinary Storage Service

Media processing and optimization service.
25GB free tier for images and videos.
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import Optional, Dict, Any
from datetime import datetime

from ..core.config import settings


def is_cloudinary_enabled() -> bool:
    """Check if Cloudinary is enabled in configuration."""
    return (
        settings.CLOUDINARY_ENABLED
        and settings.CLOUDINARY_CLOUD_NAME
        and settings.CLOUDINARY_API_KEY
        and settings.CLOUDINARY_API_SECRET
    )


def configure_cloudinary():
    """Configure Cloudinary with credentials."""
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


class CloudinaryService:
    """Cloudinary service for media storage and optimization."""
    
    def __init__(self):
        if is_cloudinary_enabled():
            configure_cloudinary()
    
    async def upload_image(
        self,
        file_path: str,
        public_id: Optional[str] = None,
        folder: str = "office_suite",
        transformation: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Upload an image to Cloudinary with automatic optimization.
        
        Args:
            file_path: Local path to the image file
            public_id: Optional custom public ID
            folder: Folder to store the image in
            transformation: Optional transformation parameters
            
        Returns:
            Dict with upload result including URLs
        """
        if not is_cloudinary_enabled():
            return {
                "success": False,
                "error": "Cloudinary is not enabled",
                "service": "cloudinary",
            }
        
        try:
            upload_params = {
                "folder": folder,
                "resource_type": "image",
                "use_filename": True,
                "unique_filename": True,
                "overwrite": False,
            }
            
            if public_id:
                upload_params["public_id"] = public_id
            
            if transformation:
                upload_params["transformation"] = transformation
            
            result = cloudinary.uploader.upload(file_path, **upload_params)
            
            return {
                "success": True,
                "service": "cloudinary",
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "width": result.get("width"),
                "height": result.get("height"),
                "format": result.get("format"),
                "bytes": result.get("bytes"),
                "uploaded_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "cloudinary",
            }
    
    async def upload_video(
        self,
        file_path: str,
        public_id: Optional[str] = None,
        folder: str = "office_suite/videos",
    ) -> Dict[str, Any]:
        """
        Upload a video to Cloudinary with automatic transcoding.
        
        Args:
            file_path: Local path to the video file
            public_id: Optional custom public ID
            folder: Folder to store the video in
            
        Returns:
            Dict with upload result
        """
        if not is_cloudinary_enabled():
            return {
                "success": False,
                "error": "Cloudinary is not enabled",
                "service": "cloudinary",
            }
        
        try:
            upload_params = {
                "folder": folder,
                "resource_type": "video",
                "use_filename": True,
                "unique_filename": True,
                "overwrite": False,
            }
            
            if public_id:
                upload_params["public_id"] = public_id
            
            result = cloudinary.uploader.upload(file_path, **upload_params)
            
            return {
                "success": True,
                "service": "cloudinary",
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "duration": result.get("duration"),
                "format": result.get("format"),
                "bytes": result.get("bytes"),
                "uploaded_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "cloudinary",
            }
    
    def generate_optimized_url(
        self,
        public_id: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        quality: str = "auto",
        format: str = "auto",
        crop: str = "fill",
    ) -> str:
        """
        Generate an optimized image URL with transformations.
        
        Args:
            public_id: Public ID of the image
            width: Target width in pixels
            height: Target height in pixels
            quality: Quality setting (default: auto)
            format: Output format (default: auto for WebP/AVIF)
            crop: Crop mode (default: fill)
            
        Returns:
            Optimized image URL
        """
        if not is_cloudinary_enabled():
            return ""
        
        transformation = {
            "quality": quality,
            "fetch_format": format,
            "crop": crop,
        }
        
        if width:
            transformation["width"] = width
        if height:
            transformation["height"] = height
        
        return cloudinary.utils.cloudinary_url(public_id, transformation=transformation)[0]
    
    def generate_thumbnail_url(
        self,
        public_id: str,
        width: int = 200,
        height: int = 200,
    ) -> str:
        """
        Generate a thumbnail URL.
        
        Args:
            public_id: Public ID of the image
            width: Thumbnail width (default: 200px)
            height: Thumbnail height (default: 200px)
            
        Returns:
            Thumbnail URL
        """
        return self.generate_optimized_url(
            public_id,
            width=width,
            height=height,
            crop="thumb",
            quality="auto",
        )
    
    async def delete_asset(self, public_id: str, resource_type: str = "image") -> Dict[str, Any]:
        """
        Delete an asset from Cloudinary.
        
        Args:
            public_id: Public ID of the asset to delete
            resource_type: Type of resource (image or video)
            
        Returns:
            Dict with deletion result
        """
        if not is_cloudinary_enabled():
            return {
                "success": False,
                "error": "Cloudinary is not enabled",
                "service": "cloudinary",
            }
        
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
            
            return {
                "success": result.get("result") == "ok",
                "service": "cloudinary",
                "public_id": public_id,
                "result": result.get("result"),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "cloudinary",
            }
    
    async def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get Cloudinary storage usage statistics.
        
        Returns:
            Dict with storage statistics
        """
        if not is_cloudinary_enabled():
            return {
                "success": False,
                "error": "Cloudinary is not enabled",
                "service": "cloudinary",
            }
        
        try:
            usage = cloudinary.api.usage()
            
            return {
                "success": True,
                "service": "cloudinary",
                "used_bytes": usage.get("usage", {}).get("storage", 0),
                "used_gb": usage.get("usage", {}).get("storage", 0) / (1024**3),
                "total_gb": 25,  # Free tier limit
                "bandwidth_used": usage.get("usage", {}).get("bandwidth", 0),
                "resource_count": usage.get("resources", 0),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "cloudinary",
            }


# Singleton instance
cloudinary_service = CloudinaryService()


async def upload_to_cloudinary(
    file_path: str,
    public_id: Optional[str] = None,
    folder: str = "office_suite",
    resource_type: str = "image",
) -> Dict[str, Any]:
    """Convenience function for uploading to Cloudinary."""
    if resource_type == "video":
        return await cloudinary_service.upload_video(file_path, public_id, folder)
    else:
        return await cloudinary_service.upload_image(file_path, public_id, folder)


async def delete_from_cloudinary(
    public_id: str,
    resource_type: str = "image",
) -> Dict[str, Any]:
    """Convenience function for deleting from Cloudinary."""
    return await cloudinary_service.delete_asset(public_id, resource_type)
