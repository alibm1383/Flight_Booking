from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, Literal
from datetime import date


class ChangePassword(BaseModel):
    CurrentPassword: str = Field(..., description="User's current password")
    NewPassword: str = Field(..., min_length=8, max_length=72, description="New password")
    ConfirmNewPassword: str = Field(..., min_length=8, max_length=72, description="Confirm new password")

    @model_validator(mode='after')
    def verify_password_match(self):
        if self.NewPassword != self.ConfirmNewPassword:
            raise ValueError("New password and its confirmation do not match.")
        return self


class CustomerProfileUpdate(BaseModel):
    FirstName: Optional[str] = Field(None, min_length=2, max_length=200, description="Customer's new first name")
    LastName: Optional[str] = Field(None, min_length=2, max_length=200, description="Customer's new last name")
    BirthDate: Optional[date] = Field(None, description="New birth date")
    Gender: Optional[Literal[0, 1]] = Field(None, description="Gender: 0 for male, 1 for female")
    Email: Optional[EmailStr] = Field(None, description="User's new email")


class AirlineProfileUpdate(BaseModel):
    CompanyName: Optional[str] = Field(None, min_length=3, max_length=200, description="Airline's new company name")
    Email: Optional[EmailStr] = Field(None, description="Airline's new email")


class AdminProfileUpdate(BaseModel):
    FirstName: Optional[str] = Field(None, min_length=2, max_length=200, description="Admin's new first name")
    LastName: Optional[str] = Field(None, min_length=2, max_length=200, description="Admin's new last name")
    BirthDate: Optional[date] = Field(None, description="Birth date")
    Gender: Optional[Literal[0, 1]] = Field(None, description="Gender")
    Email: Optional[EmailStr] = Field(None, description="Admin's new email")


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


class AvatarUploadResponse(BaseModel):
    message: str = Field(..., description="Success message for the operation")
    ImageUrl: str = Field(..., description="URL of the uploaded image")