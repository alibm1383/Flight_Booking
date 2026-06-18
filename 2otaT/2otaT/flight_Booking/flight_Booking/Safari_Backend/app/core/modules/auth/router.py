from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.modules.auth import schemas, services
from app.database import get_db

from app.core.modules.users import models
from app.core import security

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/register/customer", 
    response_model=schemas.Token, 
    status_code=status.HTTP_201_CREATED,
    summary="ثبت‌نام مسافر جدید",
    description="این متد اطلاعات مسافر را دریافت کرده و پس از ساخت پروفایل، توکن JWT را برای ورود مستقیم برمی‌گرداند."
)
def register_customer(customer_data: schemas.CustomerRegister, db: Session = Depends(get_db)):

    return services.register_customer(db, customer_data)


@router.post(
    "/register/airline", 
    response_model=schemas.Token, 
    status_code=status.HTTP_201_CREATED,
    summary="ثبت‌نام شرکت هواپیمایی",
    description="ثبت‌نام نمایندگی‌های فروش ایرلاین‌ها با دریافت نام شرکت."
)
def register_airline(airline_data: schemas.AirlineRegister, db: Session = Depends(get_db)):
    return services.register_airline(db, airline_data)


@router.post(
    "/login", 
    response_model=schemas.Token, 
    status_code=status.HTTP_200_OK,
    summary="ورود به سامانه",
    description="ورود تمامی کاربران (مسافر، ایرلاین و ادمین) با استفاده از شماره موبایل و رمز عبور."
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return services.authenticate_user(db, form_data)


# only for test
@router.get("/me", response_model=None)
def get_my_profile(current_user: models.User = Depends(security.get_current_user)):
    """
    تست مسیر محافظت شده: 
    فقط در صورتی اجرا می‌شود که توکن معتبر در هدر ارسال شده باشد.
    """
    return {
        "Id": current_user.Id,
        "PhoneNumber": current_user.PhoneNumber,
        "RoleId": current_user.RoleId,
        "IsActive": current_user.IsActive
    }