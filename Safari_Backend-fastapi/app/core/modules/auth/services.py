from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from fastapi.security import OAuth2PasswordRequestForm

from app.core.modules.users import models
from app.core.modules.auth import schemas
from app.core import security 


def check_user_exists(db: Session, phone_number: str, email: str = None):
    """بررسی تکراری بودن شماره تلفن و ایمیل (در صورت وجود)"""
    user_with_phone = db.query(models.User).filter(models.User.PhoneNumber == phone_number).first()
    if user_with_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="کاربری با این شماره تلفن قبلاً در سامانه ثبت شده است."
        )
        
    if email:
        user_with_email = db.query(models.User).filter(models.User.Email == email).first()
        if user_with_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="این ایمیل قبلاً در سامانه ثبت شده است."
            )

def get_role_id(db: Session, role_name: str) -> int:
    """پیدا کردن شناسه نقش بر اساس نام"""
    role = db.query(models.Role).filter(models.Role.Name == role_name).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"نقش '{role_name}' در دیتابیس یافت نشد. لطفاً دیتابیس را بررسی کنید."
        )
    return role.Id


def register_user(db: Session, user_data: schemas.UserRegister):

    check_user_exists(db, user_data.PhoneNumber, user_data.Email)

    role_id = get_role_id(db, "Customer")

    hashed_password = security.get_password_hash(user_data.Password)

    new_user = models.User(
        RoleId=role_id,
        PhoneNumber=user_data.PhoneNumber,
        Email=user_data.Email,
        PasswordHash=hashed_password,
        IsActive=True,
        IsEmailVerified=False,
        IsPhoneVerified=False,
        CreatedAt=datetime.now(timezone.utc)
    )
    
    db.add(new_user)
    db.flush() 

    new_customer = models.Customer(
        UserId=new_user.Id,
        FirstName=user_data.FirstName,
        LastName=user_data.LastName,
        BirthDate=user_data.BirthDate,
        Gender=user_data.Gender
    )
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_user)
    
    access_token = security.create_access_token(
        data={"user_id": new_user.Id, "role_id": new_user.RoleId}
    )
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(db: Session, form_data: OAuth2PasswordRequestForm):
    
    user = db.query(models.User).filter(models.User.PhoneNumber == form_data.username).first()
    
    if not user or not security.verify_password(form_data.password, user.PasswordHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="شماره تلفن یا رمز عبور اشتباه است.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user.LastLoginAt = datetime.now(timezone.utc)
    db.commit()

    access_token = security.create_access_token(
        data={"user_id": user.Id, "role_id": user.RoleId}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}