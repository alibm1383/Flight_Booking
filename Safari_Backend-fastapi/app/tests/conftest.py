import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timezone

from app.main import app
from app.database import Base, get_db

# Test database engine setup (SQLite In-Memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture for managing database session in tests
@pytest.fixture(scope="function")
def db_session():
    # Create all tables in the test database before each test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test to prevent interference with the next test
        Base.metadata.drop_all(bind=engine)

# Client fixture and replacement of test database with main database (Dependency Override)
@pytest.fixture(scope="function")
def client(db_session):
    # Function to override the database dependency
    def override_get_db():
        yield db_session
        
    # Tell FastAPI: "during tests, whenever get_db is called, give the temporary database"
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
        
    # Clear override settings after test ends
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def create_test_user(db_session):
    def _create_user(role_id: int = 3, is_active: bool = True):
        # Import models inside a function to avoid Circular Import errors
        from app.core.modules.users import models
        
        unique_id = uuid.uuid4().hex[:8]
        user = models.User(
            RoleId=role_id,
            PhoneNumber=f"0912{unique_id}", 
            Email=f"test_{unique_id}@example.com", 
            PasswordHash="hashed_password",
            IsActive=is_active,
            CreatedAt=datetime.now(timezone.utc)
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
        
    return _create_user

# Automatic fixture for creating base roles in test database
@pytest.fixture(scope="function", autouse=True)
def create_roles(db_session):
    """Create base roles in the test database before each test"""
    from app.core.modules.users import models
    if not db_session.query(models.Role).filter(models.Role.Id == 1).first():
        db_session.add(models.Role(Id=1, Name="Admin"))
    if not db_session.query(models.Role).filter(models.Role.Id == 2).first():
        db_session.add(models.Role(Id=2, Name="Airline"))
    if not db_session.query(models.Role).filter(models.Role.Id == 3).first():
        db_session.add(models.Role(Id=3, Name="Customer"))
    db_session.commit()