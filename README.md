# Smart House API

This project simulates a smart house system with functionality for managing houses, rooms, and devices. It includes endpoints for creating, reading, updating, and deleting houses, rooms, and devices, as well as managing users associated with the houses.

## Main File (`main.py`)

The main file contains the FastAPI app and routes for managing various entities within the smart house system. 

### Features:
- **User Management**: Create and manage users.
- **House Management**: Create and manage houses that users own.
- **Room Management**: Create and manage rooms within houses.
- **Device Management**: Add and manage devices (e.g., sensors) in rooms.
  
Each entity (user, house, room, and device) has basic CRUD functionality, allowing you to create, read, update, and delete them via the API.

### Routes:
- `POST /users`: Create a new user.
- `GET /users/{id}`: Retrieve a user by their ID.
- `PATCH /users/{id}`: Update user details.
- `DELETE /users/{id}`: Delete a user.
  
- `POST /houses`: Create a new house.
- `GET /houses/{id}`: Retrieve a house by its ID.
- `PATCH /houses/{id}`: Update a house's information.
- `DELETE /houses/{id}`: Delete a house.
  
- `POST /rooms`: Create a new room in a house.
- `GET /rooms/{id}`: Retrieve a room by its ID.
- `PATCH /rooms/{id}`: Update a room's information.
- `DELETE /rooms/{id}`: Delete a room.
  
- `POST /devices`: Create a new device (e.g., temperature sensor).
- `GET /devices/{id}`: Retrieve a device by its ID.
- `PATCH /devices/{id}`: Update a device's value.
- `DELETE /devices/{id}`: Delete a device.

## Test File (`test.py`)

The `test.py` file contains tests for all the main API routes using **pytest** and **FastAPI's TestClient**. These tests ensure the API endpoints function as expected.

### Features:
- **User Tests**: Tests for creating, reading, updating, and deleting users.
- **House Tests**: Tests for creating, reading, updating, and deleting houses.
- **Room Tests**: Tests for creating, reading, updating, and deleting rooms.
- **Device Tests**: Tests for creating, reading, updating, and deleting devices.

Each test is written to check the successful creation, retrieval, updating, and deletion of entities. For example:
- **Create**: Verifies that a new user, house, room, or device can be created with the correct data.
- **Read**: Verifies that existing users, houses, rooms, and devices can be retrieved correctly.
- **Update**: Verifies that users, houses, rooms, and devices can be updated with new data.
- **Delete**: Verifies that users, houses, rooms, and devices can be deleted.

### How to Run Tests:
To run the tests, ensure that you have **pytest** installed. Then, run the following command:

```bash
pytest test.py
