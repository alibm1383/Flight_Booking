from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.core import security
from app.core.modules.users import models, schemas, services

router = APIRouter(
    prefix="/users",
    tags=["User Management (Admin Only)"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/customers",
    response_model=schemas.PaginatedCustomersResponse,
    status_code=status.HTTP_200_OK,
    summary="Get paginated list of customers",
    description="Retrieve a paginated list of all customer users with optional search filter. Admin access only."
)
def get_customers(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search query for name, family, or phone number"),
    current_admin: models.User = Depends(security.get_current_admin),
    db: Session = Depends(get_db)
):
    return services.get_all_customers(db=db, page=page, size=size, search=search)


@router.get(
    "/airlines",
    response_model=schemas.PaginatedAirlinesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get paginated list of airlines",
    description="Retrieve a paginated list of all airline users with optional search filter. Admin access only."
)
def get_airlines(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search query for company name or phone number"),
    current_admin: models.User = Depends(security.get_current_admin),
    db: Session = Depends(get_db)
):
    return services.get_all_airlines(db=db, page=page, size=size, search=search)


@router.get(
    "/customers/{customer_id}",
    response_model=schemas.CustomerAdminResponse,
    status_code=status.HTTP_200_OK,
    summary="Get customer details by ID",
    description="Retrieve full details of a specific customer by their user ID. Admin access only."
)
def get_customer_details(
    customer_id: int,
    current_admin: models.User = Depends(security.get_current_admin),
    db: Session = Depends(get_db)
):
    return services.get_customer_by_id(db=db, target_user_id=customer_id)


@router.get(
    "/airlines/{airline_id}",
    response_model=schemas.AirlineAdminResponse,
    status_code=status.HTTP_200_OK,
    summary="Get airline details by ID",
    description="Retrieve full details of a specific airline by their user ID. Admin access only."
)
def get_airline_details(
    airline_id: int,
    current_admin: models.User = Depends(security.get_current_admin),
    db: Session = Depends(get_db)
):
    return services.get_airline_by_id(db=db, target_user_id=airline_id)


@router.patch(
    "/{user_id}/status",
    response_model=schemas.UserActionResponse,
    status_code=status.HTTP_200_OK,
    summary="Toggle user activation or approve airline",
    description="Update IsActive status for a user (block/deactivate or activate/approve). Admin access only."
)
def update_user_status(
    user_id: int,
    status_update: schemas.UserStatusUpdate,
    current_admin: models.User = Depends(security.get_current_admin),
    db: Session = Depends(get_db)
):
    return services.toggle_user_status(
        db=db,
        target_user_id=user_id,
        status_update=status_update,
        current_admin=current_admin
    )