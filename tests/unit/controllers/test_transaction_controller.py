import datetime

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from configs.database import get_db
from main import app
from src.models.base import Base
from src.models.user import User
from src.requests.transaction_request import TransactionRequest

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


def test_store_should_return_422():
    transaction_request = {
        "user_id": 1,
        "amount": 100,
        "date": "2024-10-07T02:13:18.522Z",
        "type": "credit",
        "exttrid": "12345",
        "description": "Test transaction",
    }

    response = client.post("/transactions", json=transaction_request)

    assert response.status_code == 422


def test_store_should_return_201():
    db = next(override_get_db())
    user = User(
        id=1,
        first_name="test",
        last_name="test",
        email="testuser@example.com",
        password="fakehashedpassword",
        active_status=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id == 1

    transaction_request = {
        "user_id": user.id,
        "amount": 100,
        "date": "2024-10-07T02:13:18.522Z",
        "type": "credit",
        "exttrid": "12345",
        "description": "Test transaction",
    }

    response = client.post("/transactions", json=transaction_request)

    assert response.status_code == 201
