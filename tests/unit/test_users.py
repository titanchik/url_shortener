from unittest.mock import Mock, patch
from fastapi import HTTPException
from src.routers.users import create_user, read_current_user
from src import schemas, models

# Тест создания пользователя (юнит-тест)
@patch("src.routers.users.hash_password")
def test_create_user_unit(mock_hash):
    # Настраиваем моки
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    mock_hash.return_value = "hashedpassword"
    
    user_data = schemas.UserCreate(
        email="test@example.com",
        password="testpassword"
    )
    
    # Вызываем тестируемую функцию
    result = create_user(user=user_data, db=mock_db)
    
    # Проверяем результаты
    assert result.email == user_data.email
    assert result.hashed_password == "hashedpassword"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

# Тест создания дубликата пользователя
def test_create_duplicate_user_unit():
    # Настраиваем мок с существующим пользователем
    mock_db = Mock()
    mock_user = models.User(email="exists@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    user_data = schemas.UserCreate(
        email="exists@example.com",
        password="testpassword"
    )
    
    # Проверяем, что вызовется исключение
    with pytest.raises(HTTPException) as exc_info:
        create_user(user=user_data, db=mock_db)
    
    assert exc_info.value.status_code == 400
    assert "Email already registered" in exc_info.value.detail

# Тест получения текущего пользователя
def test_read_current_user_unit():
    mock_user = models.User(email="test@example.com", id=1)
    
    result = read_current_user(current_user=mock_user)
    
    assert result.email == mock_user.email
    assert result.id == mock_user.id