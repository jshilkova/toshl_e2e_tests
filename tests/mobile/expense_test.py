import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selene import browser, have

from toshl_finance_demo.data import category
from toshl_finance_demo.data.user import User

user = User.create()


@allure.feature('Mobile entries')
@allure.story('Expense')
@allure.label('microservice', 'MEntry')
@allure.label('owner', 'allure8')
@allure.tag('smoke', 'regress', 'mobile')
@allure.label('layer', 'mobile')
class TestExpense:
    @allure.title('Add expense')
    @allure.severity('blocker')
    def test_add_expense(self, mobile_management, remove_all_entries, login_with_test_user):
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


def click_add_expense_button():
    add_expense_button_rect = browser.element((AppiumBy.ID, 'addItemButton')).locate().rect
    x = add_expense_button_rect['x'] + 75  # Well enough for typical environment
    y = add_expense_button_rect['y'] + add_expense_button_rect['height']
    action = TouchAction(browser.driver)
    action.press(None, x, y, 1)
    action.move_to(None, x + 10, y - 10)
    action.release()
    action.perform()


def enter_amount(amount: int):
    for digit in str(amount):
        browser.element((AppiumBy.ID, f'keypad_{digit}')).click()
