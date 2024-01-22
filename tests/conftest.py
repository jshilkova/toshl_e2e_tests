import allure
import pytest
import requests

from config import API_URL
from toshl_finance_demo_test.data.context import Context
from toshl_finance_demo_test.data.user import test_user
from toshl_finance_demo_test.utils.api import get_all_entries
from toshl_finance_demo_test.utils.attach import attach_request_and_response_data, \
    log_request_and_response_data_to_console


def pytest_addoption(parser):
    parser.addoption(
        '--context',
        type=Context,
        choices=list(Context),
        default=Context.CLOUD,
        help='Run tests locally or in cloud services'
    )


@pytest.fixture(scope="function", autouse=False)
def session():
    with allure.step("Login to Toshl Finance"):
        s = requests.Session()
        s.hooks['response'] += [attach_request_and_response_data, log_request_and_response_data_to_console]
        s.post(url=f'{API_URL}/oauth2/login',
               data={"email": test_user.email,
                     "password": test_user.password})
    return s


@pytest.fixture(scope="function", autouse=False)
def remove_all_entries(session):
    with allure.step("Remove all entries from test account"):
        entries = get_all_entries(session)
        for entry in entries:
            session.delete(url=f'{API_URL}/api/entries/{entry["id"]}')
