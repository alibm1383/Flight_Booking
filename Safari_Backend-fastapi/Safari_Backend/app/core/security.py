from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.core.modules.users import models

from enum import IntEnum

class RoleType(IntEnum):
    ADMIN = 1
    AIRLINE = 2
    CUSTOMER = 3

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_password_hash(password: str) -> str:
    safe_password = password[:72] 
    return pwd_context.hash(safe_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
   
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token validation failed (possibly expired or tampered).",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            raise credentials_exception
        
        if isinstance(user_id, str):
            user_id = int(user_id)
            
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.Id == user_id).first()
    if user is None:
        raise credentials_exception
        
    if not user.IsActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been blocked or deactivated by admin."
        )
        
    return user

def get_current_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.RoleId != RoleType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is only authorized for system administrator."
        )
    return current_user

def get_current_airline(current_user: models.User = Depends(get_current_user)):
    if current_user.RoleId != RoleType.AIRLINE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This operation is only authorized for airlines."
        )
    return current_user