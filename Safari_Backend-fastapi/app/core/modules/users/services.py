import logging
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.core.modules.users import models
from app.core.modules.users import schemas

logger = logging.getLogger(__name__)


def get_all_customers(db: Session, page: int = 1, size: int = 10, search: str = None):
    if page < 1 or size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page and size parameters must be greater than 0."
        )

    query = db.query(models.User).filter(models.User.RoleId == 3).options(joinedload(models.User.customer))

    if search:
        search_term = f"%{search}%"
        query = query.join(models.Customer).filter(
            or_(
                models.User.PhoneNumber.ilike(search_term),
                models.Customer.FirstName.ilike(search_term),
                models.Customer.LastName.ilike(search_term)
            )
        )

    total_records = query.count()

    offset_value = (page - 1) * size
    users = query.order_by(models.User.CreatedAt.desc()).offset(offset_value).limit(size).all()

    items = []
    for user in users:
        items.append(schemas.CustomerAdminResponse(
            Id=user.Id,
            RoleId=user.RoleId,
            PhoneNumber=user.PhoneNumber,
            Email=user.Email,
            IsActive=user.IsActive,
            CreatedAt=user.CreatedAt,
            LastLoginAt=user.LastLoginAt,
            FirstName=user.customer.FirstName if user.customer else "Unknown",
            LastName=user.customer.LastName if user.customer else "Unknown",
            BirthDate=user.customer.BirthDate if user.customer else None,
            Gender=user.customer.Gender if user.customer else 0
        ))

    return schemas.PaginatedCustomersResponse(
        items=items,
        total=total_records,
        page=page,
        size=size
    )


def get_all_airlines(db: Session, page: int = 1, size: int = 10, search: str = None):
    if page < 1 or size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page and size parameters must be greater than 0."
        )

    query = db.query(models.User).filter(models.User.RoleId == 2).options(joinedload(models.User.airline))

    if search:
        search_term = f"%{search}%"
        query = query.join(models.Airline).filter(
            or_(
                models.User.PhoneNumber.ilike(search_term),
                models.Airline.CompanyName.ilike(search_term)
            )
        )

    total_records = query.count()

    offset_value = (page - 1) * size
    users = query.order_by(models.User.CreatedAt.desc()).offset(offset_value).limit(size).all()

    items = []
    for user in users:
        items.append(schemas.AirlineAdminResponse(
            Id=user.Id,
            RoleId=user.RoleId,
            PhoneNumber=user.PhoneNumber,
            Email=user.Email,
            IsActive=user.IsActive,
            CreatedAt=user.CreatedAt,
            LastLoginAt=user.LastLoginAt,
            CompanyName=user.airline.CompanyName if user.airline else "Unknown"
        ))

    return schemas.PaginatedAirlinesResponse(
        items=items,
        total=total_records,
        page=page,
        size=size
    )


def get_customer_by_id(db: Session, target_user_id: int) -> schemas.CustomerAdminResponse:
    user = db.query(models.User).filter(
        models.User.Id == target_user_id,
        models.User.RoleId == 3
    ).options(joinedload(models.User.customer)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested customer was not found in the system."
        )

    return schemas.CustomerAdminResponse(
        Id=user.Id,
        RoleId=user.RoleId,
        PhoneNumber=user.PhoneNumber,
        Email=user.Email,
        IsActive=user.IsActive,
        CreatedAt=user.CreatedAt,
        LastLoginAt=user.LastLoginAt,
        FirstName=user.customer.FirstName if user.customer else "Unknown",
        LastName=user.customer.LastName if user.customer else "Unknown",
        BirthDate=user.customer.BirthDate if user.customer else None,
        Gender=user.customer.Gender if user.customer else 0
    )


def get_airline_by_id(db: Session, target_user_id: int) -> schemas.AirlineAdminResponse:
    user = db.query(models.User).filter(
        models.User.Id == target_user_id,
        models.User.RoleId == 2
    ).options(joinedload(models.User.airline)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested airline company was not found in the system."
        )

    return schemas.AirlineAdminResponse(
        Id=user.Id,
        RoleId=user.RoleId,
        PhoneNumber=user.PhoneNumber,
        Email=user.Email,
        IsActive=user.IsActive,
        CreatedAt=user.CreatedAt,
        LastLoginAt=user.LastLoginAt,
        CompanyName=user.airline.CompanyName if user.airline else "Unknown"
    )


def toggle_user_status(db: Session, target_user_id: int, status_update: schemas.UserStatusUpdate, current_admin: models.User):
    if target_user_id == current_admin.Id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate or block your own admin account!"
        )

    target_user = db.query(models.User).filter(models.User.Id == target_user_id).first()
    
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested user was not found in the system."
        )
    
    target_user.IsActive = status_update.IsActive
    
    try:
        db.commit()
        db.refresh(target_user)
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while updating status for user {target_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while saving the new status."
        )
    
    action_text = "activated/approved" if status_update.IsActive else "blocked/deactivated"
    message = f"User account has been successfully {action_text}."

    return schemas.UserActionResponse(
        message=message,
        UserId=target_user.Id,
        IsActive=target_user.IsActive,
        RoleId=target_user.RoleId
    )