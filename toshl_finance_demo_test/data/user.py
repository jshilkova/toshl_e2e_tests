from dataclasses import dataclass
import config


@dataclass
class User:
    email: str
    password: str
    name: str
    account: str

    @staticmethod
    def create():
        email = config.TEST_USER_EMAIL
        password = config.TEST_USER_PASSWORD
        name = config.TEST_USER_NAME
        account = config.TEST_USER_ACCOUNT
        return User(email=email, password=password, name=name, account=account)


test_user = User.create()
