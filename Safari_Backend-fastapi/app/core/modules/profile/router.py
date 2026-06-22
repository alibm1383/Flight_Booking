from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core import security
from app.core.modules.users import models
from app.core.modules.profile import schemas, services

router = APIRouter(
    prefix="/profile",
    tags=["User Profile"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/me", 
    response_model=schemas.ProfileResponse, 
    status_code=status.HTTP_200_OK,
    summary="دریافت اطلاعات پروفایل من",
    description="این مسیر توکن را بررسی کرده و اطلاعات هویتی کاربر (مسافر، ایرلاین یا ادمین) را برمی‌گرداند."
)
def get_my_profile(current_user: models.User = Depends(security.get_current_user)):
    return services.get_user_profile(current_user)


@router.put(
    "/change-password", 
    status_code=status.HTTP_200_OK,
    summary="تغییر رمز عبور",
    description="دریافت رمز عبور فعلی و تغییر آن به رمز جدید."
)
def change_password(
    password_data: schemas.ChangePassword, 
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    return services.change_user_password(db, current_user, password_data)


@router.put(
    "/update/customer", 
    response_model=schemas.ProfileResponse, 
    status_code=status.HTTP_200_OK,
    summary="ویرایش پروفایل مسافر",
)
def update_customer_profile(
    update_data: schemas.CustomerProfileUpdate, 
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.RoleId != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="شما مجوز ویرایش پروفایل مسافر را ندارید."
        )
    return services.update_customer_profile(db, current_user, update_data)


@router.put(
    "/update/airline", 
    response_model=schemas.ProfileResponse, 
    status_code=status.HTTP_200_OK,
    summary="ویرایش پروفایل شرکت هواپیمایی",
)
def update_airline_profile(
    update_data: schemas.AirlineProfileUpdate, 
    current_user: models.User = Depends(security.get_current_airline),
    db: Session = Depends(get_db)
):
    return services.update_airline_profile(db, current_user, update_data)


@router.put(
    "/update/admin", 
    response_model=schemas.ProfileResponse, 
    status_code=status.HTTP_200_OK,
    summary="ویرایش پروفایل ادمین",
)
def update_admin_profile(
    update_data: schemas.AdminProfileUpdate, 
    current_user: models.User = Depends(security.get_current_admin),
    db: Session = Depends(get_db)
):
    return services.update_admin_profile(db, current_user, update_data)