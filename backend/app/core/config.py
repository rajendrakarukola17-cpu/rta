"""
Office Suite Configuration

Environment-based configuration with validation.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Office Suite"
    APP_VERSION: str = "7.2"
    DEBUG: bool = False
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    POSTGRES_USER: str = Field(default="office_user", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="office_suite", env="POSTGRES_DB")
    
    # Redis
    REDIS_URL: str = Field(..., env="REDIS_URL")
    REDIS_PASSWORD: str = Field(..., env="REDIS_PASSWORD")
    
    # MinIO (Primary Local Storage)
    MINIO_ENDPOINT: str = Field(default="localhost:9000", env="MINIO_ENDPOINT")
    MINIO_ACCESS_KEY: str = Field(..., env="MINIO_ROOT_USER")
    MINIO_SECRET_KEY: str = Field(..., env="MINIO_ROOT_PASSWORD")
    MINIO_BUCKET_DOCUMENTS: str = "documents"
    MINIO_BUCKET_TEMP: str = "temp-uploads"
    MINIO_BUCKET_IMAGES: str = "images"
    MINIO_USE_SSL: bool = False
    
    # Cloudinary (Media Processing - 25GB Free)
    CLOUDINARY_ENABLED: bool = False
    CLOUDINARY_CLOUD_NAME: Optional[str] = Field(None, env="CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: Optional[str] = Field(None, env="CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: Optional[str] = Field(None, env="CLOUDINARY_API_SECRET")
    
    # Box (Enterprise Docs - 10GB Free)
    BOX_ENABLED: bool = False
    BOX_CLIENT_ID: Optional[str] = Field(None, env="BOX_CLIENT_ID")
    BOX_CLIENT_SECRET: Optional[str] = Field(None, env="BOX_CLIENT_SECRET")
    BOX_FOLDER_ID: str = Field(default="0", env="BOX_FOLDER_ID")
    
    # Mega Cloud (Encrypted Backup - 25GB Free)
    MEGA_ENABLED: bool = False
    MEGA_EMAIL: Optional[str] = Field(None, env="MEGA_EMAIL")
    MEGA_PASSWORD: Optional[str] = Field(None, env="MEGA_PASSWORD")
    MEGA_BACKUP_PATH: str = "/OfficeSuite/backups"
    
    # pCloud (Personal Sync - 10GB Free)
    PCLOUD_ENABLED: bool = False
    PCLOUD_USERNAME: Optional[str] = Field(None, env="PCLOUD_USERNAME")
    PCLOUD_PASSWORD: Optional[str] = Field(None, env="PCLOUD_PASSWORD")
    PCLOUD_FOLDER_ID: str = Field(default="0", env="PCLOUD_FOLDER_ID")
    
    # ImageKit (Image Processing - 20GB Free)
    IMAGEKIT_ENABLED: bool = False
    IMAGEKIT_PUBLIC_KEY: Optional[str] = Field(None, env="IMAGEKIT_PUBLIC_KEY")
    IMAGEKIT_PRIVATE_KEY: Optional[str] = Field(None, env="IMAGEKIT_PRIVATE_KEY")
    IMAGEKIT_URL_ENDPOINT: Optional[str] = Field(None, env="IMAGEKIT_URL_ENDPOINT")
    
    # Backblaze B2 (Secondary Backup - 10GB Free)
    B2_ENABLED: bool = False
    B2_APPLICATION_KEY_ID: Optional[str] = Field(None, env="B2_APPLICATION_KEY_ID")
    B2_APPLICATION_KEY: Optional[str] = Field(None, env="B2_APPLICATION_KEY")
    B2_BUCKET: str = "office-suite-b2"
    
    # Cloudflare R2 (CDN - 10GB Free)
    R2_ENABLED: bool = False
    R2_ACCOUNT_ID: Optional[str] = Field(None, env="R2_ACCOUNT_ID")
    R2_ACCESS_KEY_ID: Optional[str] = Field(None, env="R2_ACCESS_KEY_ID")
    R2_SECRET_ACCESS_KEY: Optional[str] = Field(None, env="R2_SECRET_ACCESS_KEY")
    R2_BUCKET: str = "office-suite-r2"
    R2_ENDPOINT: Optional[str] = Field(None, env="R2_ENDPOINT")
    
    # Storj (Decentralized - 25GB Free)
    STORJ_ENABLED: bool = False
    STORJ_ACCESS_KEY: Optional[str] = Field(None, env="STORJ_ACCESS_KEY")
    STORJ_BUCKET: str = "office-suite-storj"
    STORJ_ENDPOINT: str = "https://gateway.storjshare.io"
    
    # IBM COS (Compliance Archive - Free Tier)
    IBM_COS_ENABLED: bool = False
    IBM_COS_API_KEY: Optional[str] = Field(None, env="IBM_COS_API_KEY")
    IBM_COS_SERVICE_INSTANCE_ID: Optional[str] = Field(None, env="IBM_COS_SERVICE_INSTANCE_ID")
    IBM_COS_BUCKET: str = "office-suite-archive"
    IBM_COS_ENDPOINT: str = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
    IBM_COS_REGION: str = "us-south"
    
    # Tigris (Edge CDN - 5GB Free)
    TIGRIS_ENABLED: bool = False
    TIGRIS_ACCESS_KEY: Optional[str] = Field(None, env="TIGRIS_ACCESS_KEY")
    TIGRIS_SECRET_KEY: Optional[str] = Field(None, env="TIGRIS_SECRET_KEY")
    TIGRIS_BUCKET: str = "office-suite-tigris"
    TIGRIS_ENDPOINT: str = "https://fly.storage.tigris.dev"
    
    # Neon (Branching DB - 5GB Free)
    NEON_ENABLED: bool = False
    NEON_API_KEY: Optional[str] = Field(None, env="NEON_API_KEY")
    NEON_PROJECT_ID: Optional[str] = Field(None, env="NEON_PROJECT_ID")
    NEON_DATABASE_URL: Optional[str] = Field(None, env="NEON_DATABASE_URL")
    
    # Sia (Decentralized - 50GB Free)
    SIA_ENABLED: bool = False
    SIA_HOST: Optional[str] = Field(None, env="SIA_HOST")
    SIA_API_KEY: Optional[str] = Field(None, env="SIA_API_KEY")
    
    # Box Dev (API Overflow - 10GB Free)
    BOX_DEV_ENABLED: bool = False
    BOX_DEV_CLIENT_ID: Optional[str] = Field(None, env="BOX_DEV_CLIENT_ID")
    BOX_DEV_CLIENT_SECRET: Optional[str] = Field(None, env="BOX_DEV_CLIENT_SECRET")
    
    # Vercel Blob (Frontend Thumbnails - 1GB Free)
    VERCEL_BLOB_ENABLED: bool = False
    VERCEL_BLOB_TOKEN: Optional[str] = Field(None, env="VERCEL_BLOB_TOKEN")
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # Search & Vector
    TYPESENSE_API_KEY: Optional[str] = Field(None, env="TYPESENSE_API_KEY")
    TYPESENSE_HOST: Optional[str] = Field(None, env="TYPESENSE_HOST")
    QDRANT_HOST: Optional[str] = Field(None, env="QDRANT_HOST")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
