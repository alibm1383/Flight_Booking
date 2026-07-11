import os
import uuid
import shutil
import logging
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, UploadFile

from app.core.modules.users import models
from app.core.modules.profile import schemas
from app.core import security
from app.core.config import settings

logger = logging.getLogger(__name__)


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


def upload_avatar_service(db: Session, current_user: models.User, file: UploadFile) -> dict:
    
    MAX_FILE_SIZE = 2 * 1024 * 1024 
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size is too large. Maximum allowed size is 2 MB."
        )

    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    allowed_mime_types = {"image/jpeg", "image/png", "image/webp"}
    
    file_ext = f".{file.filename.split('.')[-1].lower()}"
    
    if file_ext not in allowed_extensions or file.content_type not in allowed_mime_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File format is not allowed. Only image files (png, jpg, webp) are accepted."
        )

    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = settings.UPLOADS_DIR / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Error saving avatar {unique_filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error occurred while saving the file."
        )

    if current_user.ImageUrl:
        old_filename = Path(current_user.ImageUrl).name
        old_file_path = settings.UPLOADS_DIR / old_filename
        
        if old_file_path.exists():
            try:
                os.remove(old_file_path)
            except Exception as e:
                logger.warning(f"Failed to delete old avatar {old_filename} for user {current_user.Id}: {str(e)}")
                
    image_url = f"/static/uploads/{unique_filename}"
    current_user.ImageUrl = image_url
    
    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile picture uploaded and updated successfully.",
        "ImageUrl": image_url
    }


def delete_avatar_service(db: Session, current_user: models.User):
    if not current_user.ImageUrl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You currently have no profile picture."
        )
    
    filename = Path(current_user.ImageUrl).name
    file_path = settings.UPLOADS_DIR / filename
    
    if file_path.exists():
        try:
            os.remove(file_path)
        except Exception as e:
            logger.error(f"Failed to delete avatar {filename} for user {current_user.Id}: {str(e)}")
            
    current_user.ImageUrl = None
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Your profile picture was successfully removed."}


def change_user_password(db: Session, current_user: models.User, password_data: schemas.ChangePassword):
    if not security.verify_password(password_data.CurrentPassword, current_user.PasswordHash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect."
        )
    
    current_user.PasswordHash = security.get_password_hash(password_data.NewPassword)
    
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving the new password."
        )
    
    return {"message": "Your password has been changed successfully."}


def _check_and_update_base_user(db: Session, current_user: models.User, update_data):
    update_dict = update_data.model_dump(exclude_unset=True)
    
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No new information was provided for update."
        )
    
    if "Email" in update_dict and update_dict["Email"] is not None:
        if update_dict["Email"] != current_user.Email:
            existing_email = db.query(models.User).filter(models.User.Email == update_dict["Email"]).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This email is already registered by another user."
                )
            current_user.Email = update_dict["Email"]
        
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
        raise HTTPException(status_code=500, detail="Data integrity error in the database.")
        
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
        raise HTTPException(status_code=500, detail="Data integrity error in the database.")
        
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
        raise HTTPException(status_code=500, detail="Data integrity error in the database.")
        
    return get_user_profile(current_user)