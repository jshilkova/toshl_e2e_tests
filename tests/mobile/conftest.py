import allure
import allure_commons
import pytest
from _pytest.stash import StashKey
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, support, be

from toshl_finance_demo.data.context import Context
from toshl_finance_demo.data.user import User
from toshl_finance_demo.utils import attach
from .config import load_config

config_key = StashKey()


def pytest_configure(config):
    context = config.getoption('--context')
    config.stash[config_key] = load_config(context)


@pytest.fixture(scope='function', autouse=True)
def mobile_management(pytestconfig):
    config = pytestconfig.stash[config_key]

    browser.config.timeout = config.timeout

    with allure.step('Init app session'):
        browser.config.driver = webdriver.Remote(
            config.remote_url,
            options=config.to_driver_options()
        )

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    attach.add_screenshot(browser)
    attach.add_screen_xml_dump(browser)
    session_id = browser.driver.session_id

    with allure.step('Tear down app sessioncwith id' + session_id):
        browser.quit()

    if pytestconfig.getoption('--context') == Context.CLOUD:
        attach.add_bstack_video(session_id, config.options.bs_username, config.options.bs_password)


@pytest.fixture(scope='function', autouse=False)
def login_with_test_user():
    user = User.create()
    login(user)


def login(user):
    with allure.step('Login with test user'):
        browser.element((AppiumBy.ID, "btnLogin")).click()
        browser.element((AppiumBy.ID, "btnLogin")).click()
        browser.element((AppiumBy.ID, "etEmail")).type(user.email)
        browser.element((AppiumBy.ID, "etPassword")).type(user.password)
        browser.element((AppiumBy.ID, "bLogIn")).click()

        package = browser.driver.current_package
        browser.wait_until((AppiumBy.XPATH, '//android.widget.TextView[@text="I’m syncing..."]'))
        browser.element((AppiumBy.XPATH, '//android.widget.TextView[@text="I’m syncing..."]')).should(be.not_.present)

        # The application has a bug: after the very first login it shows a gray screen
        # It works properly after restart. So we do the restart.
        browser.driver.terminate_app(package, timeout=3000)
        browser.driver.activate_app(package)
        browser.element((AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='Menu']")).should(be.present)
