from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal
from datetime import date

class CustomerRegister(BaseModel):
    PhoneNumber: str = Field(..., pattern=r"^09\d{9}$", description="11-digit phone number")
    Password: str = Field(..., min_length=8, max_length=72, description="Password at least 8 characters")
    Email: Optional[EmailStr] = Field(None, description="Optional email")
    
    FirstName: str = Field(..., min_length=2, max_length=200, description="First name")
    LastName: str = Field(..., min_length=2, max_length=200, description="Last name")
    BirthDate: Optional[date] = Field(None, description="Birth date (optional)")
    Gender: Literal[0, 1] = Field(..., description="Gender: 0 for male, 1 for female")


class AirlineRegister(BaseModel):
    PhoneNumber: str = Field(..., pattern=r"^09\d{9}$", description="11-digit phone number")
    Password: str = Field(..., min_length=8, max_length=72, description="Password at least 8 characters")
    Email: Optional[EmailStr] = Field(None, description="Optional email")
    
    CompanyName: str = Field(..., min_length=3, max_length=200, description="Company name")


class UserLogin(BaseModel):
    PhoneNumber: str = Field(..., pattern=r"^09\d{9}$", description="Phone number")
    Password: str = Field(..., description="Password")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role_id: Optional[int] = None  