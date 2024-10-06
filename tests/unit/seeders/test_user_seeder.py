# tests/unit/seeder/test_user_seeder.py
import pytest

from seeders.user_seeder import UserSeeder
from src.models import User


def test_user_seeder(db_session):
    """Test the UserSeeder to ensure it adds a user to the test database."""
    # Ensure no user exists before running the seeder
    initial_user_count = db_session.query(User).count()
    assert initial_user_count == 0, "No users should exist before seeding."

    seeder = UserSeeder(db_session=db_session)

    # Run the seeder
    seeder.run()

    # Check if the user was added
    user = db_session.query(User).filter(User.email == "test@gmail.com").first()

    # Assertions
    assert user is not None, "User should have been added to the database"
    assert user.first_name == "test", "User first name should match"
    assert user.last_name == "test", "User last name should match"
    assert user.email == "test@gmail.com", "User email should match"
    assert user.password != "test", "User password should be hashed"
    assert user.password is not None, "User password should not be None"

    # Print the user's ID and name
    print(f"User ID: {user.id}, User Name: {user.first_name} {user.last_name}")

    final_user_count = db_session.query(User).count()
    assert (
        final_user_count == initial_user_count + 1
    ), "One user should have been added to the database."
