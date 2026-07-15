from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal
from datetime import datetime, date


class UserStatusUpdate(BaseModel):
    IsActive: bool = Field(..., description="New user status (true for active/approved, false for blocked)")


class UserSearchParams(BaseModel):
    SearchQuery: Optional[str] = Field(None, description="Search by first name, last name, company name, or phone number")


class CustomerAdminResponse(BaseModel):
    Id: int = Field(..., description="General user ID")
    RoleId: int = Field(..., description="User role ID (always 3 for customer)")  
    PhoneNumber: str = Field(..., description="User phone number")
    Email: Optional[EmailStr] = Field(None, description="User email")
    IsActive: bool = Field(..., description="User active or blocked status")
    CreatedAt: datetime = Field(..., description="Registration date and time")
    LastLoginAt: Optional[datetime] = Field(None, description="Last login time")
    
    FirstName: str = Field(..., description="Customer first name")
    LastName: str = Field(..., description="Customer last name")
    BirthDate: Optional[date] = Field(None, description="Customer birth date")
    Gender: Literal[0, 1] = Field(..., description="Customer gender (0: male, 1: female)")  

    class Config:
        from_attributes = True


class AirlineAdminResponse(BaseModel):
    Id: int = Field(..., description="General user ID")
    RoleId: int = Field(..., description="User role ID (always 2 for airline)")  
    PhoneNumber: str = Field(..., description="Company phone number")
    Email: Optional[EmailStr] = Field(None, description="Company email")
    IsActive: bool = Field(..., description="Airline company approval/active status")
    CreatedAt: datetime = Field(..., description="Company registration date and time")
    LastLoginAt: Optional[datetime] = Field(None, description="Company last login time")
    
    CompanyName: str = Field(..., description="Airline company name")

    class Config:
        from_attributes = True


class PaginatedCustomersResponse(BaseModel):
    items: List[CustomerAdminResponse] = Field(..., description="List of customers on current page")
    total: int = Field(..., description="Total number of customers in database")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")


class PaginatedAirlinesResponse(BaseModel):
    items: List[AirlineAdminResponse] = Field(..., description="List of airlines on current page")
    total: int = Field(..., description="Total number of airlines in database")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")


class UserActionResponse(BaseModel):
    message: str = Field(..., description="Success message for the operation")
    UserId: int = Field(..., description="Managed user ID")
    IsActive: bool = Field(..., description="New user status in database")
    RoleId: int = Field(..., description="The role ID of the managed user")