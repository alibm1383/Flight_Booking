from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core import security
from app.core.modules.users import models

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/me")
def get_my_profile(
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    customer = db.query(models.Customer).filter(
        models.Customer.UserId == current_user.Id
    ).first()

    # نام role بر اساس RoleId
    role_map = {1: "Admin", 2: "Airline", 3: "Customer"}
    role_name = role_map.get(current_user.RoleId, "Customer")

    return {
        "first_name": customer.FirstName if customer else None,
        "last_name": customer.LastName if customer else None,
        "email": current_user.Email,
        "phone": current_user.PhoneNumber,
        "birth_date": str(customer.BirthDate) if customer and customer.BirthDate else None,
        "gender": customer.Gender if customer else None,
        "avatar": current_user.ImageUrl,
        "is_email_verified": current_user.IsEmailVerified,
        "is_phone_verified": current_user.IsPhoneVerified,
        "role": role_name,
    }
