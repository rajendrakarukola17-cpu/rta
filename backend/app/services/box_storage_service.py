"""
Box Storage Service

Enterprise document storage and collaboration.
10GB free tier for team documents.
"""
from boxsdk import Client, OAuth2
from boxsdk.exception import BoxAPIException
from typing import Optional, Dict, Any, List
from datetime import datetime
import os

from ..core.config import settings


def is_box_enabled() -> bool:
    """Check if Box is enabled in configuration."""
    return (
        settings.BOX_ENABLED
        and settings.BOX_CLIENT_ID
        and settings.BOX_CLIENT_SECRET
    )


class BoxStorageService:
    """Box storage service for enterprise document storage."""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Box client with developer token or OAuth."""
        if not is_box_enabled():
            return
        
        try:
            # For development/testing, you can use a developer token
            # In production, implement proper OAuth2 flow
            auth = OAuth2(
                client_id=settings.BOX_CLIENT_ID,
                client_secret=settings.BOX_CLIENT_SECRET,
            )
            
            # Note: This requires user authentication in production
            # For now, we'll use a placeholder
            # You need to implement proper OAuth2 token exchange
            self.client = None  # Will be initialized with valid token
            
        except Exception as e:
            print(f"Error initializing Box client: {e}")
            self.client = None
    
    def get_client_with_token(self, access_token: str) -> Client:
        """
        Create a Box client with a valid access token.
        
        Args:
            access_token: Valid Box OAuth2 access token
            
        Returns:
            Authenticated Box client
        """
        auth = OAuth2(
            client_id=settings.BOX_CLIENT_ID,
            client_secret=settings.BOX_CLIENT_SECRET,
            access_token=access_token,
        )
        return Client(auth)
    
    async def upload_file(
        self,
        file_path: str,
        folder_id: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload a file to Box.
        
        Args:
            file_path: Local path to the file
            folder_id: Box folder ID to upload to (default: root)
            access_token: OAuth2 access token (required)
            
        Returns:
            Dict with upload result
        """
        if not is_box_enabled():
            return {
                "success": False,
                "error": "Box is not enabled",
                "service": "box",
            }
        
        if not access_token:
            return {
                "success": False,
                "error": "Access token required for Box API",
                "service": "box",
            }
        
        try:
            client = self.get_client_with_token(access_token)
            folder_id = folder_id or settings.BOX_FOLDER_ID
            
            # Get folder
            folder = client.folder(folder_id)
            
            # Upload file
            filename = os.path.basename(file_path)
            new_file = folder.upload(file_path, filename)
            
            # Get item info
            file_info = new_file.get()
            
            return {
                "success": True,
                "service": "box",
                "file_id": file_info["id"],
                "file_name": file_info["name"],
                "size": file_info.get("size", 0),
                "url": file_info.get("shared_link", {}).get("url", ""),
                "folder_id": folder_id,
                "uploaded_at": datetime.utcnow().isoformat(),
            }
        except BoxAPIException as e:
            return {
                "success": False,
                "error": f"Box API error: {e.message}",
                "service": "box",
                "status_code": e.status,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "box",
            }
    
    async def download_file(
        self,
        file_id: str,
        download_path: str,
        access_token: str,
    ) -> Dict[str, Any]:
        """
        Download a file from Box.
        
        Args:
            file_id: Box file ID
            download_path: Local path to save the file
            access_token: OAuth2 access token
            
        Returns:
            Dict with download result
        """
        if not is_box_enabled():
            return {
                "success": False,
                "error": "Box is not enabled",
                "service": "box",
            }
        
        try:
            client = self.get_client_with_token(access_token)
            box_file = client.file(file_id)
            
            # Download file
            with open(download_path, 'wb') as f:
                box_file.download_to(f)
            
            return {
                "success": True,
                "service": "box",
                "file_id": file_id,
                "download_path": download_path,
            }
        except BoxAPIException as e:
            return {
                "success": False,
                "error": f"Box API error: {e.message}",
                "service": "box",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "box",
            }
    
    async def delete_file(
        self,
        file_id: str,
        access_token: str,
    ) -> Dict[str, Any]:
        """
        Delete a file from Box.
        
        Args:
            file_id: Box file ID
            access_token: OAuth2 access token
            
        Returns:
            Dict with deletion result
        """
        if not is_box_enabled():
            return {
                "success": False,
                "error": "Box is not enabled",
                "service": "box",
            }
        
        try:
            client = self.get_client_with_token(access_token)
            box_file = client.file(file_id)
            box_file.delete()
            
            return {
                "success": True,
                "service": "box",
                "file_id": file_id,
            }
        except BoxAPIException as e:
            return {
                "success": False,
                "error": f"Box API error: {e.message}",
                "service": "box",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "box",
            }
    
    async def list_files(
        self,
        folder_id: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List files in a Box folder.
        
        Args:
            folder_id: Box folder ID (default: root)
            access_token: OAuth2 access token
            
        Returns:
            Dict with list of files
        """
        if not is_box_enabled():
            return {
                "success": False,
                "error": "Box is not enabled",
                "service": "box",
            }
        
        if not access_token:
            return {
                "success": False,
                "error": "Access token required for Box API",
                "service": "box",
            }
        
        try:
            client = self.get_client_with_token(access_token)
            folder_id = folder_id or settings.BOX_FOLDER_ID
            
            folder = client.folder(folder_id)
            items = folder.get_items(limit=100)
            
            files = []
            for item in items:
                if item.type == 'file':
                    files.append({
                        "file_id": item.id,
                        "name": item.name,
                        "size": item.size,
                        "modified_at": item.modified_at.isoformat() if item.modified_at else None,
                    })
            
            return {
                "success": True,
                "service": "box",
                "folder_id": folder_id,
                "files": files,
                "count": len(files),
            }
        except BoxAPIException as e:
            return {
                "success": False,
                "error": f"Box API error: {e.message}",
                "service": "box",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "box",
            }
    
    async def create_shared_link(
        self,
        file_id: str,
        access_token: str,
        access_level: str = "open",
    ) -> Dict[str, Any]:
        """
        Create a shared link for a Box file.
        
        Args:
            file_id: Box file ID
            access_token: OAuth2 access token
            access_level: Access level (open, company, collaborators)
            
        Returns:
            Dict with shared link
        """
        if not is_box_enabled():
            return {
                "success": False,
                "error": "Box is not enabled",
                "service": "box",
            }
        
        try:
            client = self.get_client_with_token(access_token)
            box_file = client.file(file_id)
            
            # Create shared link
            updated_file = box_file.update_info({
                'shared_link': {
                    'access': access_level
                }
            })
            
            return {
                "success": True,
                "service": "box",
                "file_id": file_id,
                "shared_url": updated_file.shared_link.url,
                "access_level": access_level,
            }
        except BoxAPIException as e:
            return {
                "success": False,
                "error": f"Box API error: {e.message}",
                "service": "box",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "box",
            }
    
    async def get_storage_stats(self, access_token: str) -> Dict[str, Any]:
        """
        Get Box storage usage statistics.
        
        Args:
            access_token: OAuth2 access token
            
        Returns:
            Dict with storage statistics
        """
        if not is_box_enabled():
            return {
                "success": False,
                "error": "Box is not enabled",
                "service": "box",
            }
        
        try:
            client = self.get_client_with_token(access_token)
            user = client.user().get()
            
            used_bytes = user.get("space_used", 0)
            total_bytes = user.get("space_amount", 10 * 1024**3)  # 10GB free tier
            
            return {
                "success": True,
                "service": "box",
                "used_bytes": used_bytes,
                "used_gb": used_bytes / (1024**3),
                "total_gb": total_bytes / (1024**3),
                "percent_used": (used_bytes / total_bytes * 100) if total_bytes > 0 else 0,
            }
        except BoxAPIException as e:
            return {
                "success": False,
                "error": f"Box API error: {e.message}",
                "service": "box",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service": "box",
            }


# Singleton instance
box_service = BoxStorageService()


async def upload_to_box(
    file_path: str,
    folder_id: Optional[str] = None,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function for uploading to Box."""
    return await box_service.upload_file(file_path, folder_id, access_token)


async def download_from_box(
    file_id: str,
    download_path: str,
    access_token: str,
) -> Dict[str, Any]:
    """Convenience function for downloading from Box."""
    return await box_service.download_file(file_id, download_path, access_token)


async def delete_from_box(
    file_id: str,
    access_token: str,
) -> Dict[str, Any]:
    """Convenience function for deleting from Box."""
    return await box_service.delete_file(file_id, access_token)
