from dataclasses import dataclass
import config


@dataclass
class User:
    email: str
    password: str
    name: str

    @staticmethod
    def create():
        email = config.TEST_USER_EMAIL
        password = config.TEST_USER_PASSWORD
        name = config.TEST_USER_NAME
        return User(email=email, password=password, name=name)


test_user = User.create()
