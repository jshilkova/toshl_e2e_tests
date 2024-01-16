import allure

from toshl_finance_demo.components.left_panel import LeftPanel
from toshl_finance_demo.components.right_panel import RightPanel
from toshl_finance_demo.pages.login_page import LoginPage
from .conftest import test_user

right_panel = RightPanel()
login_page = LoginPage()
left_panel = LeftPanel()


def test_successful_login(setup_browser):
    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Enter username and password and submit the form"):
        login_page.type_email(test_user.email)
        login_page.type_password(test_user.password)
        login_page.submit()

    with allure.step("Verify user name in the left panel"):
        left_panel.verify_user(test_user.name)


def test_failed_login_with_incorrect_password(setup_browser, clean_session):
    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Enter username and password and submit the form"):
        login_page.type_email(test_user.email)
        login_page.type_password('wrong_password')
        login_page.submit()

    with allure.step("Verify error message"):
        login_page.should_be_opened()
        login_page.should_show_incorrect_email_or_password_error()
