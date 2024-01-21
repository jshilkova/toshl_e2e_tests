from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selene import browser


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
