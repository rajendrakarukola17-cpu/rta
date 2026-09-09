"""
Celery Worker Tasks

Background tasks for file processing and storage operations.
"""
from celery import Celery
from typing import Dict, Any
import os

from ..core.config import settings


# Create Celery app
celery_app = Celery(
    "office_suite_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks"],
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max
    worker_prefetch_multiplier=1,
)


@celery_app.task(bind=True, max_retries=3)
def process_file_upload(self, file_path: str, storage_service: str = "minio") -> Dict[str, Any]:
    """
    Process a file upload asynchronously.
    
    Args:
        file_path: Path to the file to upload
        storage_service: Target storage service
        
    Returns:
        Upload result dictionary
    """
    try:
        # Import here to avoid circular imports
        from .services.minio_service import upload_to_minio
        from .services.cloudinary_service import upload_to_cloudinary
        from .services.box_storage_service import upload_to_box
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Route to appropriate service
        if storage_service == "cloudinary":
            # Check if it's an image or video
            ext = os.path.splitext(file_path)[1].lower()
            resource_type = "video" if ext in [".mp4", ".mov", ".avi"] else "image"
            result = upload_to_cloudinary(file_path, resource_type=resource_type)
        elif storage_service == "box":
            # Box requires access token - would need to be passed in
            result = {"error": "Box upload requires access token"}
        else:
            # Default to MinIO
            object_name = os.path.basename(file_path)
            result = upload_to_minio(file_path, object_name)
        
        return result
    
    except Exception as e:
        # Retry with exponential backoff
        try:
            raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesExceededError:
            return {
                "success": False,
                "error": f"Max retries exceeded: {str(e)}",
                "service": storage_service,
            }


@celery_app.task(bind=True, max_retries=3)
def process_file_deletion(self, file_id: int, storage_service: str, object_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a file deletion asynchronously.
    
    Args:
        file_id: Database file ID
        storage_service: Storage service name
        object_info: Object information (bucket, key, etc.)
        
    Returns:
        Deletion result dictionary
    """
    try:
        from .services.minio_service import delete_from_minio
        from .services.cloudinary_service import delete_from_cloudinary
        from .services.box_storage_service import delete_from_box
        
        if storage_service == "minio":
            result = delete_from_minio(
                object_info["object_name"],
                object_info.get("bucket"),
            )
        elif storage_service == "cloudinary":
            result = delete_from_cloudinary(object_info["public_id"])
        elif storage_service == "box":
            result = delete_from_box(
                object_info["file_id"],
                object_info["access_token"],
            )
        else:
            result = {"error": f"Unknown storage service: {storage_service}"}
        
        return result
    
    except Exception as e:
        try:
            raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesExceededError:
            return {
                "success": False,
                "error": f"Max retries exceeded: {str(e)}",
            }


@celery_app.task
def generate_thumbnail(file_id: int, source_path: str, width: int = 200, height: int = 200) -> Dict[str, Any]:
    """
    Generate a thumbnail for an image file.
    
    Args:
        file_id: Database file ID
        source_path: Path to source image
        width: Thumbnail width
        height: Thumbnail height
        
    Returns:
        Thumbnail generation result
    """
    try:
        # Use Cloudinary for thumbnail generation if available
        if settings.CLOUDINARY_ENABLED:
            from .services.cloudinary_service import cloudinary_service
            
            # First upload the image
            upload_result = cloudinary_service.upload_image(source_path)
            
            if upload_result["success"]:
                thumbnail_url = cloudinary_service.generate_thumbnail_url(
                    upload_result["public_id"],
                    width=width,
                    height=height,
                )
                
                return {
                    "success": True,
                    "file_id": file_id,
                    "thumbnail_url": thumbnail_url,
                    "width": width,
                    "height": height,
                }
        
        # Fallback: local thumbnail generation would go here
        return {
            "success": False,
            "error": "No thumbnail service available",
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@celery_app.task
def sync_to_backup_services(file_id: int, source_service: str, object_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sync a file to backup storage services.
    
    This task implements the backup strategy:
    Primary: MinIO → Backup: Mega → B2 → IBM COS
    
    Args:
        file_id: Database file ID
        source_service: Source storage service
        object_info: Object information
        
    Returns:
        Sync result with list of successful backups
    """
    results = {
        "file_id": file_id,
        "backed_up_to": [],
        "failed": [],
    }
    
    # Download from source first
    # Then upload to backup services in priority order
    
    # Placeholder implementation
    # Full implementation would:
    # 1. Download from source
    # 2. Upload to Mega (if enabled)
    # 3. Upload to B2 (if enabled and Mega failed)
    # 4. Upload to IBM COS (if enabled and others failed)
    
    return results


@celery_app.task
def cleanup_temp_files older_than_hours: int = 24) -> Dict[str, Any]:
    """
    Clean up temporary files older than specified hours.
    
    Args:
        older_than_hours: Delete files older than this many hours
        
    Returns:
        Cleanup statistics
    """
    stats = {
        "files_deleted": 0,
        "bytes_freed": 0,
        "services_cleaned": [],
    }
    
    # Clean MinIO temp bucket
    try:
        from .services.minio_service import minio_service
        
        # List files in temp bucket
        list_result = minio_service.list_files(bucket="temp-uploads")
        
        if list_result["success"]:
            # Filter by age and delete
            # Placeholder - would need to check last_modified timestamp
            stats["files_deleted"] = 0
            stats["services_cleaned"].append("minio")
    
    except Exception as e:
        stats["error"] = str(e)
    
    return stats


@celery_app.task
def update_storage_stats() -> Dict[str, Any]:
    """
    Update storage usage statistics for all services.
    
    This should run periodically (e.g., every hour).
    
    Returns:
        Updated statistics for all services
    """
    stats = {}
    
    # MinIO
    try:
        from .services.minio_service import minio_service
        stats["minio"] = minio_service.get_storage_stats()
    except Exception as e:
        stats["minio"] = {"error": str(e)}
    
    # Cloudinary
    if settings.CLOUDINARY_ENABLED:
        try:
            from .services.cloudinary_service import cloudinary_service
            stats["cloudinary"] = cloudinary_service.get_storage_stats()
        except Exception as e:
            stats["cloudinary"] = {"error": str(e)}
    
    # Box
    if settings.BOX_ENABLED:
        # Would require access token
        pass
    
    return stats
