from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.modules.auth import schemas, services
from app.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/register/customer", 
    response_model=schemas.Token, 
    status_code=status.HTTP_201_CREATED,
    summary="Register new customer",
    description="This method receives customer information and after creating the profile, returns a JWT token for direct login."
)
def register_customer(customer_data: schemas.CustomerRegister, db: Session = Depends(get_db)):

    return services.register_customer(db, customer_data)


@router.post(
    "/register/airline", 
    response_model=schemas.Token, 
    status_code=status.HTTP_201_CREATED,
    summary="Register airline company",
    description="Register airline sales representatives by receiving company name."
)
def register_airline(airline_data: schemas.AirlineRegister, db: Session = Depends(get_db)):
    return services.register_airline(db, airline_data)


@router.post(
    "/login", 
    response_model=schemas.Token, 
    status_code=status.HTTP_200_OK,
    summary="Login to system",
    description="Login for all users (customer, airline, and admin) using phone number and password."
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return services.authenticate_user(db, form_data)