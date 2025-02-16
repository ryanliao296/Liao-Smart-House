from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI()

# In-memory database to be used for testing
users = []
houses = []
rooms = []
devices = []


class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(UserCreate):
    id: int
    houses: List[int] = []

class HouseCreate(BaseModel):
    name: str
    address: str
    user_id: int

class HouseResponse(HouseCreate):
    id: int
    rooms: List[int] = []

class RoomCreate(BaseModel):
    name: str
    house_id: int

class RoomResponse(RoomCreate):
    id: int
    devices: List[int] = []

class DeviceCreate(BaseModel):
    name: str
    type: str
    room_id: int
    value: int

class DeviceResponse(DeviceCreate):
    id: int
    value: int


@app.get("/")
async def read_root():
    return {"Welcome to the API"}

# User endpoints
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    user_id = len(users) + 1
    new_user = {"id": user_id, "name": user.name, "email": user.email, "houses": []}
    users.append(new_user)
    return new_user

@app.get("/users", response_model=List[UserResponse])
def get_users():
    return users

@app.get("/users/{id}", response_model=UserResponse)
def get_user(id: int):
    user = next((u for u in users if u["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{id}", response_model=UserResponse)
def update_user(id: int, user: UserCreate):
    existing_user = next((u for u in users if u["id"] == id), None)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user["name"] = user.name
    existing_user["email"] = user.email
    return existing_user

@app.delete("/users/{id}", status_code=204)
def delete_user(id: int):
    user = next((u for u in users if u["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete all houses associated with the user
    for house_id in user["houses"]:
        house = next((h for h in houses if h["id"] == house_id), None)
        if house:
            # Delete all rooms associated with the house
            for room_id in house["rooms"]:
                room = next((r for r in rooms if r["id"] == room_id), None)
                if room:
                    # Delete all devices associated with the room
                    for device_id in room["devices"]:
                        device = next((d for d in devices if d["id"] == device_id), None)
                        if device:
                            devices.remove(device)  # Remove the device
                    rooms.remove(room)  # Remove the room
            houses.remove(house)  # Remove the house

    # Remove the user
    users.remove(user)
    return {"detail": "User and all associated data deleted successfully"}


# House endpoints
@app.post("/houses", response_model=HouseResponse, status_code=status.HTTP_201_CREATED)
def create_house(house: HouseCreate):
    user = next((u for u in users if u["id"] == house.user_id), None)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    house_id = len(houses) + 1
    new_house = {
        "id": house_id,
        "name": house.name,
        "address": house.address,
        "user_id": house.user_id,
        "rooms": [],
    }
    houses.append(new_house)
    user["houses"].append(house_id)

    return new_house

@app.get("/houses", response_model=List[HouseResponse])
def get_houses():
    return houses

@app.get("/houses/{id}", response_model=HouseResponse)
def get_house(id: int):
    house = next((h for h in houses if h["id"] == id), None)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return house

@app.patch("/houses/{id}", response_model=HouseResponse)
def update_house(id: int, house: HouseCreate):
    existing_house = next((h for h in houses if h["id"] == id), None)
    if not existing_house:
        raise HTTPException(status_code=404, detail="House not found")

    existing_house["name"] = house.name
    existing_house["address"] = house.address
    return existing_house

@app.delete("/houses/{id}", status_code=204)
def delete_house(id: int):
    house = next((h for h in houses if h["id"] == id), None)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    # Delete all rooms associated with the house
    for room_id in house["rooms"]:
        room = next((r for r in rooms if r["id"] == room_id), None)
        if room:
            # Delete all devices associated with the room
            for device_id in room["devices"]:
                device = next((d for d in devices if d["id"] == device_id), None)
                if device:
                    devices.remove(device)  # Remove the device
            rooms.remove(room)  # Remove the room

    # Remove the house from the user
    user = next((u for u in users if u["id"] == house["user_id"]), None)
    if user:
        user["houses"].remove(id)

    # Remove the house
    houses.remove(house)
    return {"detail": "House and all associated data deleted successfully"}


# Room endpoints
@app.post("/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate):
    house = next((h for h in houses if h["id"] == room.house_id), None)
    if not house:
        raise HTTPException(status_code=400, detail="House does not exist")

    room_id = len(rooms) + 1
    new_room = {"id": room_id, "name": room.name, "house_id": room.house_id, "devices": []}
    rooms.append(new_room)

    house["rooms"].append(room_id)
    return new_room

@app.get("/rooms", response_model=List[RoomResponse])
def get_rooms():
    return rooms

@app.get("/rooms/{id}", response_model=RoomResponse)
def get_room(id: int):
    room = next((r for r in rooms if r["id"] == id), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.patch("/rooms/{id}", response_model=RoomResponse)
def update_room(id: int, room: RoomCreate):
    existing_room = next((r for r in rooms if r["id"] == id), None)
    if not existing_room:
        raise HTTPException(status_code=404, detail="Room not found")

    existing_room["name"] = room.name
    existing_room["house_id"] = room.house_id
    return existing_room

@app.delete("/rooms/{id}", status_code=204)
def delete_room(id: int):
    room = next((r for r in rooms if r["id"] == id), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Delete all devices associated with the room
    for device_id in room["devices"]:
        device = next((d for d in devices if d["id"] == device_id), None)
        if device:
            devices.remove(device)  # Remove the device

    # Remove the room from the house
    house = next((h for h in houses if h["id"] == room["house_id"]), None)
    if house:
        house["rooms"].remove(id)

    # Remove the room
    rooms.remove(room)
    return {"detail": "Room and all associated devices deleted successfully"}


# Device endpoints
@app.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(device: DeviceCreate):
    room = next((r for r in rooms if r["id"] == device.room_id), None)
    if not room:
        raise HTTPException(status_code=400, detail="Room does not exist")

    device_id = len(devices) + 1
    if device.type not in ["humidity", "temperature"]:
        raise HTTPException(status_code=400, detail="Invalid device type")

    new_device = {
        "id": device_id,
        "name": device.name,
        "type": device.type,
        "room_id": device.room_id,
        "value": device.value, 
    }
    devices.append(new_device)

    room["devices"].append(device_id)
    return new_device

@app.get("/devices", response_model=List[DeviceResponse])
def get_devices():
    return devices

@app.patch("/devices/{id}", response_model=DeviceResponse)
def update_device(id: int, device: DeviceCreate):
    existing_device = next((d for d in devices if d["id"] == id), None)
    if not existing_device:
        raise HTTPException(status_code=404, detail="Device not found")

    existing_device["value"] = device.value  
    return existing_device

@app.delete("/devices/{id}", status_code=204)
def delete_device(id: int):
    device = next((d for d in devices if d["id"] == id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Remove device from room's devices list
    room = next((r for r in rooms if r["id"] == device["room_id"]), None)
    if room:
        room["devices"].remove(id)

    devices.remove(device)
    return {"detail": "Device deleted successfully"}

@app.get("/devices/{id}", response_model=DeviceResponse)
def get_device(id: int):
    device = next((d for d in devices if d["id"] == id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device
