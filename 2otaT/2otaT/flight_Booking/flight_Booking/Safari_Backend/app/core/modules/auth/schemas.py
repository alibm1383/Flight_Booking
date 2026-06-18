from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal
from datetime import date

class CustomerRegister(BaseModel):
    PhoneNumber: str = Field(..., pattern=r"^09\d{9}$", description="شماره تلفن ۱۱ رقمی")
    Password: str = Field(..., min_length=8, max_length=72, description="رمز عبور حداقل ۸ کاراکتر")
    Email: Optional[EmailStr] = Field(None, description="ایمیل اختیاری")
    
    FirstName: str = Field(..., min_length=2, max_length=200, description="نام")
    LastName: str = Field(..., min_length=2, max_length=200, description="نام خانوادگی")
    BirthDate: Optional[date] = Field(None, description="تاریخ تولد (اختیاری)")
    Gender: Literal[0, 1] = Field(..., description="جنسیت: 0 برای مرد، 1 برای زن")


class AirlineRegister(BaseModel):
    PhoneNumber: str = Field(..., pattern=r"^09\d{9}$", description="شماره تلفن ۱۱ رقمی")
    Password: str = Field(..., min_length=8, max_length=72, description="رمز عبور حداقل ۸ کاراکتر")
    Email: Optional[EmailStr] = Field(None, description="ایمیل اختیاری")
    
    CompanyName: str = Field(..., min_length=3, max_length=200, description="نام شرکت")


class UserLogin(BaseModel):
    PhoneNumber: str = Field(..., pattern=r"^09\d{9}$", description="شماره تلفن")
    Password: str = Field(..., description="رمز عبور")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role_id: Optional[int] = None  