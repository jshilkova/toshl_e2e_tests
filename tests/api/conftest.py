import allure
import pytest
from config import API_URL
from toshl_finance_demo.data.user import User
from toshl_finance_demo.utils import api

test_user = User.create()


@pytest.fixture(scope="function", autouse=False)
def remove_all_entries(session):
    with allure.step("Remove all entries from test account"):
        entries = api.get_all_entries(session)
        for entry in entries:
            session.delete(url=f'{API_URL}/api/entries/{entry["id"]}')
