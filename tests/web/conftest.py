import os
import pytest
from dotenv import load_dotenv
from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import API_URL
from toshl_finance_demo_test.data.context import Context
from toshl_finance_demo_test.utils import api, attach


@pytest.fixture(scope="function", autouse=False)
def setup_browser(request):
    if request.config.getoption('--context') == Context.CLOUD:
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
        login = os.getenv('SELENOID_LOGIN')
        password = os.getenv('SELENOID_PASSWORD')
        remote_url = os.getenv('SELENOID_REMOTE_URL', 'selenoid.autotests.cloud/wd/hub')
        options.capabilities.update(selenoid_capabilities)
        driver = webdriver.Remote(
            command_executor=f"https://{login}:{password}@{remote_url}",
            options=options
        )
        browser.config.driver = driver

    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.base_url = 'https://toshl.com'

    yield

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_video(browser)
    attach.add_logs(browser)

    browser.quit()


@pytest.fixture(scope="function", autouse=False)
def browser_login(setup_browser, session):
    browser.open('/')
    auth_cookie = session.cookies.get("tu")
    browser.driver.add_cookie({"name": "tu", "value": auth_cookie})


@pytest.fixture(scope="function", autouse=False)
def remove_all_entries(session):
    entries = api.get_all_entries(session)
    for entry in entries:
        session.delete(url=f'{API_URL}/api/entries/{entry["id"]}')
