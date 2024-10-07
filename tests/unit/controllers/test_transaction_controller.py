import datetime

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from configs.database import get_db
from configs.logger import logger
from main import app
from src.models.base import Base
from src.models.user import User

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_store_should_return_400():
    transaction_request = {
        "user_id": 1,
        "amount": 100,
        "date": "2024-10-07T02:13:18.522Z",
        "type": "credit",
        "exttrid": "12345",
        "description": "Test transaction",
    }

    response = client.post("/transactions", json=transaction_request)

    assert response.status_code == 400


def test_store_should_return_201():
    db = next(override_get_db())
    new_user = User(
        id=1,
        first_name="test",
        last_name="test",
        email="testuser@example.com",
        password="fakehashedpassword",
        active_status=True,
        del_status=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    transaction_request = {
        "user_id": 1,
        "amount": 100,
        "date": "2024-10-07T02:13:18.522Z",
        "type": "credit",
        "exttrid": "12345",
        "description": "Test transaction",
    }

    response = client.post("/transactions", json=transaction_request)

    logger.info("Transaction response:", new_user.id, new_user.active_status)

    assert response.status_code == 201
