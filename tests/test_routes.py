import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.schemas.orgs import OrganizationCreate, OrganizationUpdate
from app.services.auth import create_access_token

# Create a test client for the FastAPI application
client = TestClient(app)

# Define test data for organizations
test_organization_data = [
    {
        "name": "Tech Innovations",
        "description": "A company that fosters innovation in technology.",
        "address": "123 Tech Road, Silicon Valley",
        "contact_email": "tech@techinnovations.com"
    },
    {
        "name": "Creative Hub",
        "description": "An organization dedicated to fostering creativity and arts.",
        "address": "456 Art Lane, New York City",
        "contact_email": "creativity@creativehub.org"
    }
]

def test_create_organization():
    """
    Test creating a new organization.
    """
    for org_data in test_organization_data:
        response = client.post("/orgs/", json=org_data)
        assert response.status_code == 201
        created_org = response.json()
        assert created_org["name"] == org_data["name"]
        assert created_org["description"] == org_data["description"]

def test_get_organizations():
    """
    Test retrieving all organizations.
    """
    response = client.get("/orgs/")
    assert response.status_code == 200
    orgs = response.json()
    assert len(orgs) > 0

def test_get_organization_by_id():
    """
    Test retrieving a specific organization by ID.
    """
    # Create a test organization first
    response = client.post("/orgs/", json=test_organization_data[0])
    created_org = response.json()
    
    org_id = created_org["id"]
    response = client.get(f"/orgs/{org_id}")
    assert response.status_code == 200
    retrieved_org = response.json()
    assert retrieved_org["id"] == org_id

def test_update_organization():
    """
    Test updating an existing organization.
    """
    # Create a test organization first
    response = client.post("/orgs/", json=test_organization_data[0])
    created_org = response.json()
    
    org_id = created_org["id"]
    update_data = {
        "name": "Updated Tech Innovations",
        "description": "An updated description for the tech company."
    }
    response = client.put(f"/orgs/{org_id}", json=update_data)
    assert response.status_code == 200
    updated_org = response.json()
    assert updated_org["id"] == org_id
    assert updated_org["name"] == update_data["name"]
    assert updated_org["description"] == update_data["description"]

def test_delete_organization():
    """
    Test deleting an existing organization.
    """
    # Create a test organization first
    response = client.post("/orgs/", json=test_organization_data[0])
    created_org = response.json()
    
    org_id = created_org["id"]
    response = client.delete(f"/orgs/{org_id}")
    assert response.status_code == 204
    
    # Verify that the organization has been deleted
    response = client.get(f"/orgs/{org_id}")
    assert response.status_code == 404

# Run the tests
if __name__ == "__main__":
    pytest.main()