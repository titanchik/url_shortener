import pytest
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from src.config import settings

@pytest.fixture
def auth_client(client, test_db):
    # Создаем тестового пользователя
    user_data = {
        "email": "auth@example.com",
        "password": "testpass"
    }
    client.post("/users/", json=user_data)
    
    # Получаем токен
    form_data = OAuth2PasswordRequestForm(
        username=user_data["email"],
        password=user_data["password"],
        scope=""
    )
    response = client.post("/token", data=form_data.__dict__)
    token = response.json()["access_token"]
    
    # Устанавливаем токен в клиент
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client

@pytest.fixture
def test_token(test_db):
    user_data = {
        "email": "token@example.com",
        "password": "testpass"
    }
    client.post("/users/", json=user_data)
    
    form_data = OAuth2PasswordRequestForm(
        username=user_data["email"],
        password=user_data["password"],
        scope=""
    )
    response = client.post("/token", data=form_data.__dict__)
    return response.json()["access_token"]