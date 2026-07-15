from app.main import app
from datetime import datetime, timezone
from app.core import security
from app.core.modules.users import models

# Helper function to create a user with a real hashed password
def create_valid_login_user(db_session, role_name="Customer", phone="09109998877"):
    """Create a user with a hashed password (roles are automatically created by conftest)"""
    raw_password = "StrongPassword123!"
    hashed_password = security.get_password_hash(raw_password)
    
    role_id = 3 if role_name == "Customer" else 2
    
    user = models.User(
        RoleId=role_id,
        PhoneNumber=phone,
        Email=f"valid_login_{phone}@example.com",
        PasswordHash=hashed_password,
        IsActive=True,
        CreatedAt=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user, raw_password

# Registration tests
def test_register_customer_success(client):
    """Test successful registration of a new customer with complete data"""
    payload = {
        "PhoneNumber": "09121112233",
        "Email": "new@example.com",
        "Password": "SecurePassword123!",
        "FirstName": "John",
        "LastName": "Doe",
        "Gender": 0 
    }
    response = client.post("/auth/register/customer", json=payload)
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_register_airline_success(client):
    """Test successful registration of an airline company (restored)"""
    payload = {
        "PhoneNumber": "09124445566",
        "Password": "AirlinePassword123!",
        "CompanyName": "Mahan Air"
    }
    response = client.post("/auth/register/airline", json=payload)
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_register_without_optional_email(client):
    """Test customer registration without sending the optional email field"""
    payload = {
        "PhoneNumber": "09122223344",
        "Password": "SecurePassword123!",
        "FirstName": "Jane",
        "LastName": "Doe",
        "Gender": 1 
    }
    response = client.post("/auth/register/customer", json=payload)
    assert response.status_code == 201

def test_register_duplicate_phone_number(client, db_session):
    """Test prevention of registration with a duplicate phone number"""
    existing_user, _ = create_valid_login_user(db_session, phone="09129999999")
    payload = {
        "PhoneNumber": existing_user.PhoneNumber, 
        "Password": "NewPassword123!",
        "FirstName": "Jane",
        "LastName": "Doe",
        "Gender": 1
    }
    response = client.post("/auth/register/customer", json=payload)
    assert response.status_code == 409

# Login tests
def test_login_success(client, db_session):
    """Test successful login"""
    user, raw_password = create_valid_login_user(db_session)
    response = client.post(
        "/auth/login",
        data={"username": user.PhoneNumber, "password": raw_password}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client, db_session):
    """Test unsuccessful login with wrong password (restored)"""
    user, _ = create_valid_login_user(db_session)
    response = client.post(
        "/auth/login",
        data={"username": user.PhoneNumber, "password": "WrongPassword!456"}
    )
    assert response.status_code == 401

def test_login_non_existent_user(client):
    """Test attempting to login with a number that does not exist in the system (restored)"""
    response = client.post(
        "/auth/login",
        data={"username": "09999999999", "password": "AnyPassword123!"}
    )
    assert response.status_code == 401

def test_login_inactive_user(client, db_session):
    """Test preventing login of a blocked user"""
    user, raw_password = create_valid_login_user(db_session, phone="09115556677")
    user.IsActive = False  # Block the user
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": user.PhoneNumber, "password": raw_password}
    )
    assert response.status_code == 403
    # Support both Persian and English error messages to prevent test failure
    detail = response.json()["detail"].lower()
    assert "مسدود" in detail or "deactivated" in detail

# Input validation tests (Pydantic Validation)
def test_register_invalid_password_length(client):
    """Test preventing registration with a short password (less than 8 characters)"""
    payload = {
        "PhoneNumber": "09125556677",
        "Password": "short",  # Short password
        "FirstName": "John",
        "LastName": "Doe",
        "Gender": 0 
    }
    response = client.post("/auth/register/customer", json=payload)
    assert response.status_code == 422

def test_register_invalid_phone_format(client):
    """Test registration with an invalid phone number (restored)"""
    payload = {
        "PhoneNumber": "1234567",  # Does not match the standard pattern
        "Password": "SecurePassword123!",
        "FirstName": "John",
        "LastName": "Doe",
        "Gender": 0
    }
    response = client.post("/auth/register/customer", json=payload)
    assert response.status_code == 422

def test_register_invalid_email_format(client):
    """Test registration with an invalid email (added as suggested)"""
    payload = {
        "PhoneNumber": "09121112233",
        "Email": "invalid-email",  # Invalid email
        "Password": "SecurePassword123!",
        "FirstName": "John",
        "LastName": "Doe",
        "Gender": 0
    }
    response = client.post("/auth/register/customer", json=payload)
    assert response.status_code == 422