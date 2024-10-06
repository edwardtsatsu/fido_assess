from seeders.user_seeder import UserSeeder
from src.models import User


def test_user_seeder(db_session):
    initial_user_count = db_session.query(User).count()
    assert initial_user_count == 0, "No users should exist before seeding."

    seeder = UserSeeder(db_session=db_session)

    seeder.run()

    user = db_session.query(User).filter(User.email == "test@gmail.com").first()

    assert user is not None
    assert user.first_name == "test"
    assert user.last_name == "test"
    assert user.email == "test@gmail.com"
    assert user.password != "test"
    assert user.password is not None

    print(f"User ID: {user.id}, User Name: {user.first_name} {user.last_name}")

    final_user_count = db_session.query(User).count()
    assert (
        final_user_count == initial_user_count + 1
    ), "One user should have been added to the database."
