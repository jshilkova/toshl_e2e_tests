import allure
from toshl_finance_demo_test.components import left_panel
from toshl_finance_demo_test.data.user import test_user
from toshl_finance_demo_test.pages.web import login_page


@allure.feature('Authorization')
@allure.story('Login with username and password')
@allure.label('microservice', 'Login')
@allure.label('owner', 'allure8')
@allure.tag('smoke', 'regress', 'web')
@allure.label('layer', 'web')
class TestLogin:
    @allure.title('Successful login')
    @allure.severity('blocker')
    def test_successful_login(self, setup_browser):
        with allure.step("Open login page"):
            login_page.open()

        with allure.step("Enter username and password and submit the form"):
            login_page.type_email(test_user.email)
            login_page.type_password(test_user.password)
            login_page.submit()

        with allure.step("Verify user name in the left panel"):
            left_panel.verify_user(test_user.name)

    @allure.title('Login with incorrect password')
    @allure.severity('normal')
    def test_failed_login_with_incorrect_password(self, setup_browser):
        with allure.step("Open login page"):
            login_page.open()

        with allure.step("Enter username and password and submit the form"):
            login_page.type_email(test_user.email)
            login_page.type_password('wrong_password')
            login_page.submit()

        with allure.step("Verify error message"):
            login_page.should_be_opened()
            login_page.should_show_incorrect_email_or_password_error()
