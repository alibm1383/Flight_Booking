from app.main import app
from app.core import security


# 1. Security guard and access control tests (Role-Based Access Control)
def test_rbac_non_admin_access_denied(client, create_test_user):
    """Ensure that customers and airlines are not allowed to access admin routes"""
    customer_user = create_test_user(role_id=3)
    airline_user = create_test_user(role_id=2)

    # Test 1: Customer trying to access customer list (should return 403)
    app.dependency_overrides[security.get_current_user] = lambda: customer_user
    response_customer = client.get("/users/customers")
    assert response_customer.status_code == 403

    # Test 2: Airline trying to access airline list (should return 403)
    app.dependency_overrides[security.get_current_user] = lambda: airline_user
    response_airline = client.get("/users/airlines")
    assert response_airline.status_code == 403

    app.dependency_overrides.clear()


# 2. Customer list, pagination, and invalid input tests
def test_get_customers_pagination(client, create_test_user):
    """Test advanced pagination for customer list"""
    admin_user = create_test_user(role_id=1)
    app.dependency_overrides[security.get_current_admin] = lambda: admin_user

    # Create 3 test customers in database
    for _ in range(3):
        create_test_user(role_id=3)

    # Request second page with size 2 (should return only 1 remaining record)
    response = client.get("/users/customers?page=2&size=2")
    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 3
    assert len(data["items"]) == 1
    assert data["page"] == 2

    app.dependency_overrides.clear()


def test_invalid_pagination_params(client, create_test_user):
    """Test sending invalid pagination parameters (should return validation error)"""
    admin_user = create_test_user(role_id=1)
    app.dependency_overrides[security.get_current_admin] = lambda: admin_user

    # Try to send page number zero and negative size
    response = client.get("/users/customers?page=0&size=-5")
    assert response.status_code == 422  # HTTP_422_UNPROCESSABLE_ENTITY

    app.dependency_overrides.clear()


# 3. Airline-specific tests (list and pagination)
def test_get_airlines_pagination(client, create_test_user):
    """Test fetching and pagination of airline company list"""
    admin_user = create_test_user(role_id=1)
    app.dependency_overrides[security.get_current_admin] = lambda: admin_user

    # Create 2 test airlines in database
    for _ in range(2):
        create_test_user(role_id=2)

    response = client.get("/users/airlines?page=1&size=10")
    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert response.json()["items"][0]["RoleId"] == 2

    app.dependency_overrides.clear()


# 4. Advanced search tests with database joins (Search)
def test_search_customers(client, create_test_user, db_session):
    """Test searching customers based on profile attributes"""
    admin_user = create_test_user(role_id=1)
    app.dependency_overrides[security.get_current_admin] = lambda: admin_user

    # Create a user and manually attach a Customer profile
    target_user = create_test_user(role_id=3)
    from app.core.modules.users import models
    customer_profile = models.Customer(UserId=target_user.Id, FirstName="Ali", LastName="Rezaei", Gender=0)
    db_session.add(customer_profile)
    db_session.commit()

    # Search by first name
    response = client.get("/users/customers?search=Ali")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["FirstName"] == "Ali"

    app.dependency_overrides.clear()


def test_search_airlines(client, create_test_user, db_session):
    """Test searching airlines by company name"""
    admin_user = create_test_user(role_id=1)
    app.dependency_overrides[security.get_current_admin] = lambda: admin_user

    # Create a user and manually attach an Airline profile
    target_user = create_test_user(role_id=2)
    from app.core.modules.users import models
    airline_profile = models.Airline(UserId=target_user.Id, CompanyName="Mahan Air")
    db_session.add(airline_profile)
    db_session.commit()

    # Search by company name
    response = client.get("/users/airlines?search=Mahan")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["CompanyName"] == "Mahan Air"

    app.dependency_overrides.clear()


# 5. Resource detail retrieval tests based on REST principles (Detail Endpoints)
def test_get_customer_detail_success_and_not_found(client, create_test_user):
    """Test successful and unsuccessful retrieval of a specific customer's details"""
    admin_user = create_test_user(role_id=1)
    app.dependency_overrides[security.get_current_admin] = lambda: admin_user

    target_customer = create_test_user(role_id=3)

    # Scenario 1: Successful retrieval of existing user details
    response = client.get(f"/users/customers/{target_customer.Id}")
    assert response.status_code == 200
    assert response.json()["Id"] == target_customer.Id

    # Scenario 2: Error for non-existent user
    response_404 = client.get("/users/customers/999999")
    assert response_404.status_code == 404

    app.dependency_overrides.clear()


def test_get_airline_detail(client, create_test_user):
    """Test retrieving details of an airline company by user ID"""
    admin_user = create_test_user(role_id=1)
    app.dependency_overrides[security.get_current_admin] = lambda: admin_user

    target_airline = create_test_user(role_id=2)
    
    response = client.get(f"/users/airlines/{target_airline.Id}")
    assert response.status_code == 200
    assert response.json()["Id"] == target_airline.Id

    app.dependency_overrides.clear()


# 6. User status toggle and approval tests (Toggle Status / Approve)
def test_toggle_user_status_success(client, create_test_user):
    """Test successfully blocking a customer's account by admin"""
    admin_user = create_test_user(role_id=1)
    app.dependency_overrides[security.get_current_admin] = lambda: admin_user

    target_customer = create_test_user(role_id=3, is_active=True)

    # Send PATCH request to block account (IsActive: false)
    response = client.patch(
        f"/users/{target_customer.Id}/status",
        json={"IsActive": False}
    )
    assert response.status_code == 200
    assert response.json()["IsActive"] == False
    assert response.json()["UserId"] == target_customer.Id

    app.dependency_overrides.clear()


def test_admin_cannot_block_himself(client, create_test_user):
    """Test security guard preventing admin from blocking themselves"""
    admin_user = create_test_user(role_id=1, is_active=True)
    app.dependency_overrides[security.get_current_admin] = lambda: admin_user

    # Admin trying to deactivate his own account (should return 400)
    response = client.patch(
        f"/users/{admin_user.Id}/status",
        json={"IsActive": False}
    )
    assert response.status_code == 400
    assert "own admin account" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_toggle_status_user_not_found(client, create_test_user):
    """Test trying to change status of a user that does not exist in the system"""
    admin_user = create_test_user(role_id=1)
    app.dependency_overrides[security.get_current_admin] = lambda: admin_user

    # Send PATCH request for a non-existent ID
    response = client.patch("/users/999999/status", json={"IsActive": False})
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

    app.dependency_overrides.clear()