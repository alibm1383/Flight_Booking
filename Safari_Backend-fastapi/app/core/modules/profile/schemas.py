from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, Literal
from datetime import date


class ChangePassword(BaseModel):
    CurrentPassword: str = Field(..., description="رمز عبور فعلی کاربر")
    NewPassword: str = Field(..., min_length=8, max_length=72, description="رمز عبور جدید")
    ConfirmNewPassword: str = Field(..., min_length=8, max_length=72, description="تکرار رمز عبور جدید")

    @model_validator(mode='after')
    def verify_password_match(self):
        if self.NewPassword != self.ConfirmNewPassword:
            raise ValueError("رمز عبور جدید و تکرار آن با هم مطابقت ندارند.")
        return self


class CustomerProfileUpdate(BaseModel):
    FirstName: Optional[str] = Field(None, min_length=2, max_length=200, description="نام جدید مسافر")
    LastName: Optional[str] = Field(None, min_length=2, max_length=200, description="نام خانوادگی جدید مسافر")
    BirthDate: Optional[date] = Field(None, description="تاریخ تولد جدید")
    Gender: Optional[Literal[0, 1]] = Field(None, description="جنسیت: 0 برای مرد، 1 برای زن")
    Email: Optional[EmailStr] = Field(None, description="ایمیل جدید کاربر")
    ImageUrl: Optional[str] = Field(None, max_length=1000, description="آدرس عکس پروفایل جدید")


class AirlineProfileUpdate(BaseModel):
    CompanyName: Optional[str] = Field(None, min_length=3, max_length=200, description="نام جدید شرکت هواپیمایی")
    Email: Optional[EmailStr] = Field(None, description="ایمیل جدید شرکت")
    ImageUrl: Optional[str] = Field(None, max_length=1000, description="آدرس عکس لوگو یا پروفایل جدید")


class AdminProfileUpdate(BaseModel):
    FirstName: Optional[str] = Field(None, min_length=2, max_length=200, description="نام جدید ادمین")
    LastName: Optional[str] = Field(None, min_length=2, max_length=200, description="نام خانوادگی جدید ادمین")
    BirthDate: Optional[date] = Field(None, description="تاریخ تولد")
    Gender: Optional[Literal[0, 1]] = Field(None, description="جنسیت")
    Email: Optional[EmailStr] = Field(None, description="ایمیل جدید ادمین")
    ImageUrl: Optional[str] = Field(None, max_length=1000, description="آدرس عکس پروفایل جدید")


class CustomerInfoResponse(BaseModel):
    FirstName: str
    LastName: str
    BirthDate: Optional[date] = None
    Gender: int

    class Config:
        from_attributes = True


class AirlineInfoResponse(BaseModel):
    CompanyName: str

    class Config:
        from_attributes = True


class AdminInfoResponse(BaseModel):
    FirstName: str
    LastName: str
    BirthDate: Optional[date] = None
    Gender: int

    class Config:
        from_attributes = True


class ProfileResponse(BaseModel):
    Id: int
    RoleId: int
    PhoneNumber: str
    Email: Optional[EmailStr] = None
    ImageUrl: Optional[str] = None
    
    CustomerDetails: Optional[CustomerInfoResponse] = None
    AirlineDetails: Optional[AirlineInfoResponse] = None
    AdminDetails: Optional[AdminInfoResponse] = None

    class Config:
        from_attributes = True