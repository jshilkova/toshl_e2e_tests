import json

import allure
import pytest
import requests
from allure_commons.types import AttachmentType

from config import API_URL
from toshl_finance_demo.data.user import User
from utils import api
from utils.attach import attach_request_and_response_data, log_request_and_response_data_to_console

test_user = User.create()


@pytest.fixture(scope="module", autouse=False)
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
        entries = api.get_all_entries(session)
        for entry in entries:
            session.delete(url=f'{API_URL}/api/entries/{entry["id"]}')
