"""
Database Models

SQLAlchemy models for Office Suite.
"""
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from ..core.database import Base


class User(Base):
    """User model for authentication and profile management."""
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    files: Mapped[list["File"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"


class File(Base):
    """File model for tracking stored files across multiple storage services."""
    
    __tablename__ = "files"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)  # Path/key in storage service
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)  # Size in bytes
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    storage_service: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., 'minio', 'cloudinary', 'box'
    storage_bucket: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    checksum: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # SHA-256 hash
    
    # Metadata
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Comma-separated tags
    
    # Status
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Relationships
    owner: Mapped["User"] = relationship(back_populates="files")
    
    def __repr__(self) -> str:
        return f"<File {self.filename} ({self.storage_service})>"


class StorageStats(Base):
    """Track storage usage per service."""
    
    __tablename__ = "storage_stats"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    used_bytes: Mapped[int] = mapped_column(Integer, default=0)
    total_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    file_count: Mapped[int] = mapped_column(Integer, default=0)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<StorageStats {self.service_name}>"
