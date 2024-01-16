import json
import os
from dataclasses import dataclass
from datetime import datetime
from time import sleep

import allure
import pytest
import requests
from dotenv import load_dotenv
from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
import sys
from config import API_URL
from toshl_finance_demo.data.user import User
from utils import api, attach

# from utils import attach

test_user = User.create()


def pytest_addoption(parser):
    parser.addoption(
        '--local',
        help='Run tests locally with option added',
        action='store_true'
    )


@pytest.fixture(scope="function", autouse=False)
def remove_all_entries(session):
    with allure.step("Remove all entries from test account"):
        entries = api.get_all_entries(session)
        for entry in entries:
            session.delete(url=f'{API_URL}/api/entries/{entry["id"]}')
