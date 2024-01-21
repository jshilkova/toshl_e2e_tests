from appium.webdriver.common.appiumby import AppiumBy
from selene import browser
from selenium.webdriver import ActionChains


def click_add_expense_button():
    add_expense_button_rect = browser.element((AppiumBy.ID, 'addItemButton')).locate().rect
    x = 75 - add_expense_button_rect['width'] / 2  # Well enough for typical environment
    y = add_expense_button_rect['height'] / 2 - 1

    add_button = browser.element((AppiumBy.ID, 'addItemButton')).locate()
    ActionChains(browser.driver).move_to_element_with_offset(add_button, x, y).click().perform()


def enter_amount(amount: int):
    for digit in str(amount):
        browser.element((AppiumBy.ID, f'keypad_{digit}')).click()
