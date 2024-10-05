from configs.database import db_session
from src.models.user import User
from src.utils import generate_password, hash_password


class UserSeeder:
    def __init__(self):
        self.db = db_session

    def run(self):
        existing_user = (
            self.db.query(User).filter(User.email == "test@gmail.com").first()
        )

        if existing_user is None:
            test_user_info = {
                "first_name": "test",
                "last_name": "test",
                "email": "test@gmail.com",
                "password": hash_password(generate_password()),
            }

            new_user = User(**test_user_info)

            self.db.add(new_user)
            self.db.commit()
