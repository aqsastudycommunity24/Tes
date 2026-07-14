"""Authentication API routes"""

from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import UserLogin, TokenResponse, UserCreate, UserResponse
from app.core.security import PasswordHasher, JWTHandler
from app.db.connection import get_db
from datetime import timedelta

router = APIRouter()
password_hasher = PasswordHasher()
jwt_handler = JWTHandler()


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db=Depends(get_db)):
    """
    Admin login endpoint
    
    Returns:
        - access_token: JWT access token
        - refresh_token: JWT refresh token
    """
    # Find user by email
    user = await db["users"].find_one({"email": user_data.email})
    
    if not user or not password_hasher.verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create tokens
    access_token = jwt_handler.create_access_token(
        data={"sub": str(user["_id"]), "email": user["email"], "role": user["role"]}
    )
    refresh_token = jwt_handler.create_refresh_token(
        data={"sub": str(user["_id"]), "email": user["email"]}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """
    Refresh access token using refresh token
    """
    payload = jwt_handler.decode_token(refresh_token)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    access_token = jwt_handler.create_access_token(
        data={"sub": user_id}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout():
    """
    Logout endpoint (client-side token deletion)
    """
    return {"message": "Logged out successfully"}
