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

from toshl_finance_demo.data.user import User
from utils import api, attach

# from utils import attach

API_URL = 'https://toshl.com'
test_user = User.create()


@pytest.fixture(scope="module", autouse=False)
def setup_browser(request):
    if not request.config.getoption('--local'):
        options = Options()
        selenoid_capabilities = {
            "browserName": "chrome",
            "browserVersion": "100.0",
            'selenoid:options': {
                'enableVNC': True,
                'enableVideo': True
            }
        }

        load_dotenv()
        login = os.getenv("LOGIN")
        password = os.getenv("PASSWORD")
        options.capabilities.update(selenoid_capabilities)
        driver = webdriver.Remote(
            command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
            options=options
        )
        browser.config.driver = driver

    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.base_url = 'https://toshl.com'

    yield

    browser.quit()


@pytest.fixture(scope="function", autouse=True)
def collect_test_data():
    yield

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_video(browser)
    attach.add_logs(browser)


@pytest.fixture(scope="module", autouse=False)
def session(setup_browser):
    with allure.step("Login to Toshl Finance"):
        s = requests.Session()
        resp = s.post(url=f'{API_URL}/oauth2/login',
                      data={"email": test_user.email,
                            "password": test_user.password})
        browser.open('/')
        auth_cookie = resp.cookies.get("tu")
        browser.driver.add_cookie({"name": "tu", "value": auth_cookie})
    return s


@pytest.fixture(scope="function", autouse=False)
def remove_all_entries(session):
    entries = api.get_all_entries(session)
    for entry in entries:
        session.delete(url=f'{API_URL}/api/entries/{entry["id"]}')


@pytest.fixture(scope="function", autouse=False)
def clean_session():
    browser.driver.delete_cookie("tu")
