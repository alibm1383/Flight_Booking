from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.core.modules.users import models
from app.core.modules.profile import schemas
from app.core import security


def get_user_profile(user: models.User) -> dict:
    return {
        "Id": user.Id,
        "RoleId": user.RoleId,
        "PhoneNumber": user.PhoneNumber,
        "Email": user.Email,
        "ImageUrl": user.ImageUrl,
        "CustomerDetails": user.customer if user.RoleId == 3 else None,
        "AirlineDetails": user.airline if user.RoleId == 2 else None,
        "AdminDetails": user.admin if user.RoleId == 1 else None,
    }


def change_user_password(db: Session, current_user: models.User, password_data: schemas.ChangePassword):
    if not security.verify_password(password_data.CurrentPassword, current_user.PasswordHash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رمز عبور فعلی اشتباه است."
        )
    
    current_user.PasswordHash = security.get_password_hash(password_data.NewPassword)
    
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="خطایی در ثبت رمز عبور جدید رخ داد."
        )
    
    return {"message": "رمز عبور شما با موفقیت تغییر یافت."}


def _check_and_update_base_user(db: Session, current_user: models.User, update_data):
    update_dict = update_data.model_dump(exclude_unset=True)
    
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="هیچ اطلاعات جدیدی برای به‌روزرسانی ارسال نشده است."
        )
    
    if "Email" in update_dict and update_dict["Email"] is not None:
        if update_dict["Email"] != current_user.Email:
            existing_email = db.query(models.User).filter(models.User.Email == update_dict["Email"]).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="این ایمیل توسط کاربر دیگری ثبت شده است."
                )
            current_user.Email = update_dict["Email"]
            
    if "ImageUrl" in update_dict:
        current_user.ImageUrl = update_dict["ImageUrl"]
        
    return update_dict


def update_customer_profile(db: Session, current_user: models.User, update_data: schemas.CustomerProfileUpdate):
    update_dict = _check_and_update_base_user(db, current_user, update_data)
    
    if current_user.customer:
        if "FirstName" in update_dict: current_user.customer.FirstName = update_dict["FirstName"]
        if "LastName" in update_dict: current_user.customer.LastName = update_dict["LastName"]
        if "BirthDate" in update_dict: current_user.customer.BirthDate = update_dict["BirthDate"]
        if "Gender" in update_dict: current_user.customer.Gender = update_dict["Gender"]

    try:
        db.commit()
        db.refresh(current_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="خطای یکپارچگی داده‌ها در پایگاه داده.")
        
    return get_user_profile(current_user)


def update_airline_profile(db: Session, current_user: models.User, update_data: schemas.AirlineProfileUpdate):
    update_dict = _check_and_update_base_user(db, current_user, update_data)
    
    if current_user.airline:
        if "CompanyName" in update_dict: current_user.airline.CompanyName = update_dict["CompanyName"]

    try:
        db.commit()
        db.refresh(current_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="خطای یکپارچگی داده‌ها در پایگاه داده.")
        
    return get_user_profile(current_user)


def update_admin_profile(db: Session, current_user: models.User, update_data: schemas.AdminProfileUpdate):
    update_dict = _check_and_update_base_user(db, current_user, update_data)
    
    if current_user.admin:
        if "FirstName" in update_dict: current_user.admin.FirstName = update_dict["FirstName"]
        if "LastName" in update_dict: current_user.admin.LastName = update_dict["LastName"]
        if "BirthDate" in update_dict: current_user.admin.BirthDate = update_dict["BirthDate"]
        if "Gender" in update_dict: current_user.admin.Gender = update_dict["Gender"]

    try:
        db.commit()
        db.refresh(current_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="خطای یکپارچگی داده‌ها در پایگاه داده.")
        
    return get_user_profile(current_user)