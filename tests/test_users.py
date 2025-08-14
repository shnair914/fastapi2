from app import schemas
from app.config import settings
import jwt
import pytest

def test_root(client):
    response = client.get("/")
    print(response.json().get('message'))
    assert response.json().get('message') == 'Hello World'
    assert response.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "sndart100@yahoo.com", "password": "password123"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "sndart100@yahoo.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongeemail@yahoo.com", "password123", 403),
    ("sanjeev13@yahoo.com", "wrongpassword", 403),
    ("wrongeemail@yahoo.com", "wrongpassword", 403),
    # (None, "password123", 422),
    # ("sanjeev@gmail.com", None, 422),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
  