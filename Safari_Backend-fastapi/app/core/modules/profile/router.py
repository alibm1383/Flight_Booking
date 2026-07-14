from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
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
    "/my-information", 
    response_model=schemas.ProfileResponse, 
    status_code=status.HTTP_200_OK,
    summary="Get my profile information",
    description="This endpoint validates the token and returns the user's identity information (customer, airline, or admin)."
)
def get_my_profile(current_user: models.User = Depends(security.get_current_user)):
    return services.get_user_profile(current_user)


@router.post(
    "/upload-avatar",
    response_model=schemas.AvatarUploadResponse,  
    status_code=status.HTTP_201_CREATED,
    summary="Upload profile picture",
    description="Receive the physical image file from the frontend, save it on the server, and automatically update the logged-in user's profile."
)
def upload_avatar(
    file: UploadFile = File(..., description="Profile image file"),
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    return services.upload_avatar_service(db, current_user, file)


@router.delete(
    "/remove-avatar",
    status_code=status.HTTP_200_OK,
    summary="Delete profile picture",
    description="Deletes the physical image file from the server and clears the corresponding field in the database."
)
def remove_avatar(
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    return services.delete_avatar_service(db, current_user)


@router.put(
    "/change-password", 
    status_code=status.HTTP_200_OK,
    summary="Change password",
    description="Receive current password and change it to a new one."
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
    summary="Update customer profile",
)
def update_customer_profile(
    update_data: schemas.CustomerProfileUpdate, 
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.RoleId != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update customer profile."
        )
    return services.update_customer_profile(db, current_user, update_data)


@router.put(
    "/update/airline", 
    response_model=schemas.ProfileResponse, 
    status_code=status.HTTP_200_OK,
    summary="Update airline company profile",
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
    summary="Update admin profile",
)
def update_admin_profile(
    update_data: schemas.AdminProfileUpdate, 
    current_user: models.User = Depends(security.get_current_admin),
    db: Session = Depends(get_db)
):
    return services.update_admin_profile(db, current_user, update_data)