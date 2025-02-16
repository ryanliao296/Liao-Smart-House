import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Ensure that objects are created for the tests
@pytest.fixture
def create_user():
    response = client.post("/users", json={"name": "User 1", "email": "user1@example.com"})
    return response.json()

@pytest.fixture
def create_house(create_user):
    response = client.post("/houses", json={"name": "House 1", "address": "123 Main St", "user_id": create_user["id"]})
    return response.json()

@pytest.fixture
def create_room(create_house):
    response = client.post("/rooms", json={"name": "Living Room", "house_id": create_house["id"]})
    return response.json()

@pytest.fixture
def create_device(create_room):
    response = client.post("/devices", json={
        "name": "Temperature Sensor",
        "type": "temperature",
        "room_id": create_room["id"],
        "value": 25
    })
    return response.json()  

# User tests
def test_create_user():
    response = client.post("/users", json={"name": "John Doe", "email": "john.doe@example.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john.doe@example.com"

def test_get_user(create_user):
    response = client.get(f"/users/{create_user['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == create_user["name"]
    assert response.json()["email"] == create_user["email"]

def test_update_user(create_user):
    response = client.patch(f"/users/{create_user['id']}", json={"name": "John Updated", "email": "john.updated@example.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "John Updated"
    assert response.json()["email"] == "john.updated@example.com"

def test_delete_user(create_user):
    response = client.delete(f"/users/{create_user['id']}")
    assert response.status_code == 204  



# House Tests
def test_create_house(create_user):
    response = client.post("/houses", json={"name": "House 1", "address": "123 Main St", "user_id": create_user["id"]})
    assert response.status_code == 201  
    assert response.json()["name"] == "House 1"

def test_get_house(create_house):
    response = client.get(f"/houses/{create_house['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "House 1"

def test_update_house(create_house):
    response = client.patch(
        f"/houses/{create_house['id']}",
        json={"name": "House 1 Updated", "address": "1234 Main St", "user_id": create_house["user_id"]}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "House 1 Updated"

def test_delete_house(create_house):
    response = client.delete(f"/houses/{create_house['id']}")
    assert response.status_code == 204 



# Room tests
def test_create_room(create_house):
    response = client.post("/rooms", json={"name": "Living Room", "house_id": create_house["id"]})
    assert response.status_code == 201
    assert response.json()["name"] == "Living Room"

def test_get_room(create_room):
    response = client.get(f"/rooms/{create_room['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Living Room"

def test_update_room(create_room):
    response = client.patch(
        f"/rooms/{create_room['id']}",
        json={"name": "Living Room Updated", "house_id": create_room["house_id"]}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Living Room Updated"

def test_delete_room(create_room):
    response = client.delete(f"/rooms/{create_room['id']}")
    assert response.status_code == 204  



# Device tests
def test_create_device(create_room):
    response = client.post("/devices", json={"name": "Temperature Sensor", "type": "temperature", "room_id": create_room["id"], "value": 25})
    assert response.status_code == 201
    assert response.json()["name"] == "Temperature Sensor"

def test_get_device(create_device):
    response = client.get(f"/devices/{create_device['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Temperature Sensor"

def test_update_device(create_device):
    response = client.patch(f"/devices/{create_device['id']}", json={
        "name": create_device["name"],  # Keeping the same name
        "type": create_device["type"],  # Keeping the same type
        "room_id": create_device["room_id"],  # Keeping the same room_id
        "value": 30  # Updating the value
    })
    assert response.status_code == 200
    assert response.json()["value"] == 30  # Ensure value is updated

def test_delete_device(create_device):
    response = client.delete(f"/devices/{create_device['id']}")
    assert response.status_code == 204 
