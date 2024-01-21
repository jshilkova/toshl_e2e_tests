import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have
from tests.mobile.expense_page_helper import click_add_expense_button, enter_amount
from toshl_finance_demo_test.data import category


@allure.feature('Mobile entries')
@allure.story('Expense')
@allure.suite('Add expense')
@allure.label('microservice', 'MEntry')
@allure.label('owner', 'allure8')
@allure.tag('smoke', 'regress', 'mobile')
@allure.label('layer', 'mobile')
class TestExpense:
    @allure.title('Add expense')
    @allure.severity('blocker')
    def test_add_expense_without_tag(self, mobile_management, remove_all_entries, login_with_test_user):
        with allure.step('Click on "Add Expense" button'):
            click_add_expense_button()
        with allure.step('Enter amount'):
            amount = 120
            enter_amount(amount)
        with allure.step('Submit amount'):
            browser.element((AppiumBy.ID, 'keypad_next')).click()
        with allure.step('Select category'):
            browser.element((AppiumBy.XPATH, f'//android.widget.TextView[@text="{category.charity.name}"]')).click()
        with allure.step('Submit expense'):
            browser.element((AppiumBy.ID, 'ivConfirm')).click()

        with allure.step('Verify that expense is displayed'):
            expenses = browser.all((AppiumBy.CLASS_NAME, 'android.widget.TableRow'))
            expenses.should(have.size(1))
            expenses[0].element((AppiumBy.ID, 'tvCategory')).should(have.text(category.charity.name))
            expenses[0].element((AppiumBy.ID, 'tvAmount')).should(have.text(f'GEL{amount}.00'))
