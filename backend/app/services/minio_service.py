"""
MinIO Storage Service

Primary local storage using S3-compatible MinIO.
All files start here before being distributed to other services.
"""
import aiofiles
from minio import Minio
from minio.error import S3Error
from typing import Optional, Dict, Any
import hashlib
from datetime import datetime

from ..core.config import settings


class MinIOService:
    """MinIO storage service for primary file storage."""
    
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_SSL,
        )
        self._initialize_buckets()
    
    def _initialize_buckets(self):
        """Create default buckets if they don't exist."""
        buckets = [
            settings.MINIO_BUCKET_DOCUMENTS,
            settings.MINIO_BUCKET_TEMP,
            settings.MINIO_BUCKET_IMAGES,
        ]
        
        for bucket in buckets:
            try:
                if not self.client.bucket_exists(bucket):
                    self.client.make_bucket(bucket)
            except Exception as e:
                print(f"Error creating bucket {bucket}: {e}")
    
    async def upload_file(
        self,
        file_path: str,
        object_name: str,
        bucket: Optional[str] = None,
        content_type: str = "application/octet-stream",
    ) -> Dict[str, Any]:
        """
        Upload a file to MinIO.
        
        Args:
            file_path: Local path to the file
            object_name: Name to store the file as in MinIO
            bucket: Target bucket (default: documents)
            content_type: MIME type of the file
            
        Returns:
            Dict with upload result including etag, size, and url
        """
        bucket = bucket or settings.MINIO_BUCKET_DOCUMENTS
        
        try:
            # Calculate file hash
            sha256_hash = hashlib.sha256()
            async with aiofiles.open(file_path, "rb") as f:
                content = await f.read()
                sha256_hash.update(content)
                file_size = len(content)
            
            # Upload to MinIO
            result = self.client.fput_object(
                bucket,
                object_name,
                file_path,
                content_type=content_type,
            )
            
            return {
                "success": True,
                "service": "minio",
                "bucket": bucket,
                "object_name": object_name,
                "etag": result.etag,
                "size": file_size,
                "checksum": sha256_hash.hexdigest(),
                "url": f"http://{settings.MINIO_ENDPOINT}/{bucket}/{object_name}",
                "uploaded_at": datetime.utcnow().isoformat(),
            }
        except S3Error as e:
            return {
                "success": False,
                "error": str(e),
                "service": "minio",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "minio",
            }
    
    async def download_file(
        self,
        object_name: str,
        download_path: str,
        bucket: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Download a file from MinIO.
        
        Args:
            object_name: Name of the object in MinIO
            download_path: Local path to save the file
            bucket: Source bucket (default: documents)
            
        Returns:
            Dict with download result
        """
        bucket = bucket or settings.MINIO_BUCKET_DOCUMENTS
        
        try:
            self.client.fget_object(bucket, object_name, download_path)
            
            return {
                "success": True,
                "service": "minio",
                "bucket": bucket,
                "object_name": object_name,
                "download_path": download_path,
            }
        except S3Error as e:
            return {
                "success": False,
                "error": str(e),
                "service": "minio",
            }
    
    async def delete_file(
        self,
        object_name: str,
        bucket: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Delete a file from MinIO.
        
        Args:
            object_name: Name of the object to delete
            bucket: Source bucket (default: documents)
            
        Returns:
            Dict with deletion result
        """
        bucket = bucket or settings.MINIO_BUCKET_DOCUMENTS
        
        try:
            self.client.remove_object(bucket, object_name)
            
            return {
                "success": True,
                "service": "minio",
                "bucket": bucket,
                "object_name": object_name,
            }
        except S3Error as e:
            return {
                "success": False,
                "error": str(e),
                "service": "minio",
            }
    
    async def get_file_url(
        self,
        object_name: str,
        bucket: Optional[str] = None,
        expires: int = 3600,
    ) -> Dict[str, Any]:
        """
        Get a presigned URL for temporary access.
        
        Args:
            object_name: Name of the object
            bucket: Source bucket (default: documents)
            expires: URL expiration time in seconds (default: 1 hour)
            
        Returns:
            Dict with presigned URL
        """
        bucket = bucket or settings.MINIO_BUCKET_DOCUMENTS
        
        try:
            url = self.client.presigned_get_object(
                bucket,
                object_name,
                expires=__import__("datetime").timedelta(seconds=expires),
            )
            
            return {
                "success": True,
                "service": "minio",
                "url": url,
                "expires_in": expires,
            }
        except S3Error as e:
            return {
                "success": False,
                "error": str(e),
                "service": "minio",
            }
    
    async def list_files(
        self,
        prefix: str = "",
        bucket: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List files in a bucket.
        
        Args:
            prefix: Optional prefix to filter objects
            bucket: Source bucket (default: documents)
            
        Returns:
            Dict with list of objects
        """
        bucket = bucket or settings.MINIO_BUCKET_DOCUMENTS
        
        try:
            objects = list(self.client.list_objects(bucket, prefix=prefix))
            
            files = [
                {
                    "object_name": obj.object_name,
                    "size": obj.size,
                    "etag": obj.etag,
                    "last_modified": obj.last_modified.isoformat() if obj.last_modified else None,
                }
                for obj in objects
            ]
            
            return {
                "success": True,
                "service": "minio",
                "bucket": bucket,
                "files": files,
                "count": len(files),
            }
        except S3Error as e:
            return {
                "success": False,
                "error": str(e),
                "service": "minio",
            }
    
    async def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage usage statistics.
        
        Returns:
            Dict with storage statistics
        """
        try:
            # Note: MinIO doesn't provide easy bucket size API
            # This is a placeholder - in production, you'd calculate this differently
            return {
                "success": True,
                "service": "minio",
                "endpoint": settings.MINIO_ENDPOINT,
                "buckets": [
                    settings.MINIO_BUCKET_DOCUMENTS,
                    settings.MINIO_BUCKET_TEMP,
                    settings.MINIO_BUCKET_IMAGES,
                ],
                "note": "Size calculation requires admin API access",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "minio",
            }


# Singleton instance
minio_service = MinIOService()


async def upload_to_minio(
    file_path: str,
    object_name: str,
    bucket: Optional[str] = None,
    content_type: str = "application/octet-stream",
) -> Dict[str, Any]:
    """Convenience function for uploading to MinIO."""
    return await minio_service.upload_file(file_path, object_name, bucket, content_type)


async def download_from_minio(
    object_name: str,
    download_path: str,
    bucket: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function for downloading from MinIO."""
    return await minio_service.download_file(object_name, download_path, bucket)


async def delete_from_minio(
    object_name: str,
    bucket: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function for deleting from MinIO."""
    return await minio_service.delete_file(object_name, bucket)
