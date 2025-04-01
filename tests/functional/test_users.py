import pytest
from fastapi import status
from sqlalchemy.orm import Session
from src import models, schemas
from src.database import get_db
from src.utils import hash_password

# Тест создания пользователя
def test_create_user(client, test_db):
    user_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    response = client.post("/users/", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    
    # Проверяем, что пользователь действительно создан в БД
    db: Session = next(get_db())
    db_user = db.query(models.User).filter(models.User.email == user_data["email"]).first()
    assert db_user is not None
    assert db_user.hashed_password == hash_password(user_data["password"])

# Тест дублирования email
def test_create_duplicate_user(client, test_db):
    user_data = {
        "email": "duplicate@example.com",
        "password": "testpassword"
    }
    
    # Первое создание - успешно
    response = client.post("/users/", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    
    # Второе создание - должно вернуть ошибку
    response = client.post("/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]

# Тест получения текущего пользователя (требуется аутентификация)
def test_read_current_user(client, test_db):
    # Сначала создаем пользователя
    user_data = {
        "email": "current@example.com",
        "password": "testpassword"
    }
    create_response = client.post("/users/", json=user_data)
    assert create_response.status_code == status.HTTP_200_OK
    
    # Получаем токен аутентификации
    auth_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    token_response = client.post("/token", data=auth_data)
    assert token_response.status_code == status.HTTP_200_OK
    token = token_response.json()["access_token"]
    
    # Делаем запрос к защищенному эндпоинту
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

# Тест неавторизованного доступа
def test_unauthorized_access(client, test_db):
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED