"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models import User
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenData,
    TokenRefresh,
    PasswordChange
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenData, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = AuthService.hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Generate tokens
    access_token = AuthService.create_access_token(str(new_user.id), new_user.email)
    refresh_token = AuthService.create_refresh_token(str(new_user.id))
    
    return TokenData(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/login", response_model=TokenData)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user with email and password"""
    # Find user
    result = await db.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not AuthService.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate tokens
    access_token = AuthService.create_access_token(str(user.id), user.email)
    refresh_token = AuthService.create_refresh_token(str(user.id))
    
    return TokenData(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=TokenData)
async def refresh_token(token_data: TokenRefresh):
    """Refresh access token using refresh token"""
    payload = AuthService.verify_refresh_token(token_data.refresh_token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user_id = payload.get("sub")
    email = payload.get("email")
    
    # Generate new tokens
    new_access_token = AuthService.create_access_token(user_id, email)
    new_refresh_token = AuthService.create_refresh_token(user_id)
    
    return TokenData(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(lambda: None)  # Will be implemented with security dependency
):
    """Get current authenticated user"""
    # This endpoint will be used after implementing security dependencies
    return current_user


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(lambda: None)
):
    """Change user password"""
    # Verify current password
    if not AuthService.verify_password(
        password_data.current_password,
        current_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password_hash = AuthService.hash_password(password_data.new_password)
    await db.commit()
    
    return {"message": "Password changed successfully"}
