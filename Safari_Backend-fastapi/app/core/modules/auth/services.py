from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from fastapi.security import OAuth2PasswordRequestForm

from app.core.modules.users import models
from app.core.modules.auth import schemas
from app.core import security 


def check_user_exists(db: Session, phone_number: str, email: str = None):
    user_with_phone = db.query(models.User).filter(models.User.PhoneNumber == phone_number).first()
    if user_with_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this phone number is already registered in the system."
        )
        
    if email:
        user_with_email = db.query(models.User).filter(models.User.Email == email).first()
        if user_with_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email is already registered in the system."
            )

def get_role_id(db: Session, role_name: str) -> int:
    role = db.query(models.Role).filter(models.Role.Name == role_name).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Role '{role_name}' not found in the database. Please check the database."
        )
    return role.Id


def register_customer(db: Session, customer_data: schemas.CustomerRegister):

    check_user_exists(db, customer_data.PhoneNumber, customer_data.Email)

    role_id = get_role_id(db, "Customer")

    hashed_password = security.get_password_hash(customer_data.Password)

    new_user = models.User(
        RoleId=role_id,
        PhoneNumber=customer_data.PhoneNumber,
        Email=customer_data.Email,
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
        FirstName=customer_data.FirstName,
        LastName=customer_data.LastName,
        BirthDate=customer_data.BirthDate,
        Gender=customer_data.Gender
    )
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_user)
    
    access_token = security.create_access_token(
        data={"user_id": new_user.Id, "role_id": new_user.RoleId}
    )
    return {"access_token": access_token, "token_type": "bearer"}


def register_airline(db: Session, airline_data: schemas.AirlineRegister):

    check_user_exists(db, airline_data.PhoneNumber, airline_data.Email)
    role_id = get_role_id(db, "Airline")
    hashed_password = security.get_password_hash(airline_data.Password)

    new_user = models.User(
        RoleId=role_id,
        PhoneNumber=airline_data.PhoneNumber,
        Email=airline_data.Email,
        PasswordHash=hashed_password,
        IsActive=False,
        IsEmailVerified=False,
        IsPhoneVerified=False,
        CreatedAt=datetime.now(timezone.utc)
    )
    
    db.add(new_user)
    db.flush() 

    new_airline = models.Airline(
        UserId=new_user.Id,
        CompanyName=airline_data.CompanyName
    )
    
    db.add(new_airline)
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
            detail="Phone number or password is incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.IsActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated or blocked by the admin."
        )
    
    user.LastLoginAt = datetime.now(timezone.utc)
    db.commit()

    access_token = security.create_access_token(
        data={"user_id": user.Id, "role_id": user.RoleId}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}