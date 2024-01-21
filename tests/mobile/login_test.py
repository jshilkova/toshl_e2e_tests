import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be
from tests.mobile.conftest import login
from toshl_finance_demo_test.data.user import test_user


@allure.feature('Mobile authorization')
@allure.story('Login with username and password')
@allure.label('microservice', 'MLogin')
@allure.label('owner', 'allure8')
@allure.tag('smoke', 'regress', 'mobile')
@allure.label('layer', 'mobile')
class TestLogin:
    @allure.title('Successful login')
    @allure.severity('blocker')
    def test_successful_login(self, mobile_management):
        login(test_user)

        with allure.step('Verify that user is logged in'):
            browser.element((AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='Menu']")).click()
            (browser.element((AppiumBy.XPATH, f'//android.widget.TextView[@resource-id="com.thirdframestudios.'
                                              f'android.expensoor:id/tvLeftNavItemTitle" and @text="{test_user.name}"]'))
             .should(be.present))

    @allure.title('Login with incorrect password')
    @allure.severity('normal')
    def test_failed_with_incorrect_password(self, mobile_management):
        browser.element((AppiumBy.ID, "btnLogin")).click()
        browser.element((AppiumBy.ID, "btnLogin")).click()
        browser.element((AppiumBy.ID, "etEmail")).type(test_user.email)
        browser.element((AppiumBy.ID, "etPassword")).type('wrong_password')
        browser.element((AppiumBy.ID, "bLogIn")).click()

        incorrect_password_message = "The e-mail or password you provided is not correct. Please try again."
        browser.element((AppiumBy.XPATH, f'//*[@text="{incorrect_password_message}"]')).should(be.present)
