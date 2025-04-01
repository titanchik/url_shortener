import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import Base, engine
from sqlalchemy.orm import sessionmaker

client = TestClient(app)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_short_link(test_db):
    response = client.post(
        "/links/shorten",
        json={"original_url": "https://example.com"}
    )
    assert response.status_code == 200
    assert "short_code" in response.json()