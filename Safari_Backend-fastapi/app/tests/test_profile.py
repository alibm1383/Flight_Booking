import pytest
from io import BytesIO
from datetime import datetime, timezone
from types import SimpleNamespace

from app.main import app
from app.core import security
from app.core.modules.users import models

# Bytes of a real 1x1 pixel PNG image to pass potential future validation (Magic Numbers)
MINIMAL_PNG = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'


# Profile-specific fixtures and helper functions
@pytest.fixture
def mock_uploads_dir(tmp_path, monkeypatch):
    """
    This fixture creates a temporary directory and replaces the entire settings object
    in the services module with a mock object whose UPLOADS_DIR points to tmp_path.
    """
    # Create a mock object that only has UPLOADS_DIR
    mock_settings = SimpleNamespace(UPLOADS_DIR=tmp_path)
    
    # Replace settings in the services module with the mock_settings
    monkeypatch.setattr("app.core.modules.profile.services.settings", mock_settings)
    
    return tmp_path

def create_user_with_profile(db_session, role_id=3, phone="09101112233"):
    """Create a user along with associated tables (Customer, Airline, Admin)"""
    password = "OldPassword123!"
    hashed_password = security.get_password_hash(password)
    
    user = models.User(
        RoleId=role_id,
        PhoneNumber=phone,
        Email=f"test_{phone}@example.com",
        PasswordHash=hashed_password,
        IsActive=True,
        CreatedAt=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.flush()
    
    if role_id == 3:
        profile = models.Customer(UserId=user.Id, FirstName="Old", LastName="Name", Gender=0)
    elif role_id == 2:
        profile = models.Airline(UserId=user.Id, CompanyName="Old Airline")
    elif role_id == 1:
        profile = models.Admin(UserId=user.Id, FirstName="Admin", LastName="User", Gender=1)
        
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(user)
    
    return user, password


# 1. Profile information retrieval tests
def test_get_my_information(client, db_session):
    """Test successful retrieval of profile information for logged-in user"""
    user, _ = create_user_with_profile(db_session, role_id=3)
    app.dependency_overrides[security.get_current_user] = lambda: user
    
    response = client.get("/profile/my-information")
    
    assert response.status_code == 200
    data = response.json()
    assert data["PhoneNumber"] == user.PhoneNumber
    assert data["CustomerDetails"]["FirstName"] == "Old"
    
    app.dependency_overrides.clear()


# 2. Profile update tests for different roles and password change
def test_update_customer_profile_success(client, db_session):
    """Test successful update of customer profile"""
    user, _ = create_user_with_profile(db_session, role_id=3)
    app.dependency_overrides[security.get_current_user] = lambda: user
    
    payload = {"FirstName": "NewName"}
    response = client.put("/profile/update/customer", json=payload)
    
    assert response.status_code == 200
    assert response.json()["CustomerDetails"]["FirstName"] == "NewName"
    app.dependency_overrides.clear()

def test_update_airline_profile_success(client, db_session):
    """Test successful update of airline company profile"""
    user, _ = create_user_with_profile(db_session, role_id=2)
    app.dependency_overrides[security.get_current_airline] = lambda: user
    
    payload = {"CompanyName": "New Airline Name"}
    response = client.put("/profile/update/airline", json=payload)
    
    assert response.status_code == 200
    assert response.json()["AirlineDetails"]["CompanyName"] == "New Airline Name"
    app.dependency_overrides.clear()

def test_update_admin_profile_success(client, db_session):
    """Test successful update of admin profile"""
    user, _ = create_user_with_profile(db_session, role_id=1)
    app.dependency_overrides[security.get_current_admin] = lambda: user
    
    payload = {"FirstName": "Super", "LastName": "Admin"}
    response = client.put("/profile/update/admin", json=payload)
    
    assert response.status_code == 200
    assert response.json()["AdminDetails"]["FirstName"] == "Super"
    app.dependency_overrides.clear()

def test_update_customer_wrong_role(client, db_session):
    """Test preventing customer profile update by an unauthorized role"""
    admin_user, _ = create_user_with_profile(db_session, role_id=1, phone="09110000000")
    app.dependency_overrides[security.get_current_user] = lambda: admin_user
    
    response = client.put("/profile/update/customer", json={"FirstName": "Test"})
    assert response.status_code == 403
    app.dependency_overrides.clear()

def test_update_profile_duplicate_email(client, db_session):
    """Test preventing setting an email that is already registered by another user"""
    user1, _ = create_user_with_profile(db_session, phone="09121111111")
    user2, _ = create_user_with_profile(db_session, phone="09122222222")
    
    app.dependency_overrides[security.get_current_user] = lambda: user2
    payload = {"Email": user1.Email}
    response = client.put("/profile/update/customer", json=payload)
    
    assert response.status_code == 409
    app.dependency_overrides.clear()

def test_change_password_success_and_wrong_current(client, db_session):
    """Test successful and unsuccessful password change"""
    user, password = create_user_with_profile(db_session)
    app.dependency_overrides[security.get_current_user] = lambda: user
    
    wrong_payload = {
        "CurrentPassword": "WrongPassword1!",
        "NewPassword": "NewPassword123!",
        "ConfirmNewPassword": "NewPassword123!"
    }
    response_wrong = client.put("/profile/change-password", json=wrong_payload)
    assert response_wrong.status_code == 400
    
    correct_payload = {
        "CurrentPassword": password,
        "NewPassword": "NewPassword123!",
        "ConfirmNewPassword": "NewPassword123!"
    }
    response_success = client.put("/profile/change-password", json=correct_payload)
    assert response_success.status_code == 200
    app.dependency_overrides.clear()

def test_change_password_mismatch(client, db_session):
    """Test Pydantic validation for mismatch between new password and its confirmation (restored)"""
    user, password = create_user_with_profile(db_session)
    app.dependency_overrides[security.get_current_user] = lambda: user
    
    payload = {
        "CurrentPassword": password,
        "NewPassword": "NewPassword123!",
        "ConfirmNewPassword": "DifferentPassword123!"
    }
    response = client.put("/profile/change-password", json=payload)
    assert response.status_code == 422
    
    app.dependency_overrides.clear()
    

# 3. Avatar upload and removal tests (using temporary path)
def test_upload_avatar_success(client, db_session, mock_uploads_dir):
    """Test successful upload of an image with allowed format and real PNG file"""
    user, _ = create_user_with_profile(db_session)
    app.dependency_overrides[security.get_current_user] = lambda: user
    
    # Use bytes of a real PNG image
    fake_image = BytesIO(MINIMAL_PNG)
    
    response = client.post(
        "/profile/upload-avatar",
        files={"file": ("avatar.png", fake_image, "image/png")}
    )
    
    assert response.status_code == 201
    assert "ImageUrl" in response.json()
    app.dependency_overrides.clear()

def test_upload_avatar_invalid_format(client, db_session, mock_uploads_dir):
    """Test preventing upload of non-image files (restored)"""
    user, _ = create_user_with_profile(db_session)
    app.dependency_overrides[security.get_current_user] = lambda: user
    
    fake_txt = BytesIO(b"this is a text file")
    
    response = client.post(
        "/profile/upload-avatar",
        files={"file": ("document.txt", fake_txt, "text/plain")}
    )
    
    assert response.status_code == 400
    assert "format is not allowed" in response.json()["detail"].lower()
    
    app.dependency_overrides.clear()

def test_remove_avatar_success(client, db_session, mock_uploads_dir):
    """Test successful removal of avatar for a user who has an image"""
    user, _ = create_user_with_profile(db_session)
    
    # Simulate having an avatar in the database
    filename = "test_avatar.png"
    user.ImageUrl = f"/static/uploads/{filename}"
    db_session.commit()
    
    # Create a physical file in the temporary folder so that os.remove does not fail
    fake_file_path = mock_uploads_dir / filename
    fake_file_path.write_bytes(MINIMAL_PNG)
    
    app.dependency_overrides[security.get_current_user] = lambda: user
    
    # Send the delete request
    response = client.delete("/profile/remove-avatar")
    
    assert response.status_code == 200
    assert user.ImageUrl is None  # The database field should be null
    assert not fake_file_path.exists()  # The file should be deleted from disk (temporary)
    app.dependency_overrides.clear()

def test_remove_avatar_not_found(client, db_session, mock_uploads_dir):
    """Test avatar removal when the user has no picture (404 error)"""
    user, _ = create_user_with_profile(db_session)
    app.dependency_overrides[security.get_current_user] = lambda: user
    
    response = client.delete("/profile/remove-avatar")
    
    assert response.status_code == 404
    app.dependency_overrides.clear()