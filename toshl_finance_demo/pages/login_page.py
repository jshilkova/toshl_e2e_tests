import requests
from selene import browser, be, have


class LoginPage:
    def open(self):
        browser.open('/login')

    def type_email(self, email):
        browser.element('[name="email"]').type(email)

    def type_password(self, password):
        browser.element('[name="password"]').type(password)

    def should_show_incorrect_email_or_password_error(self):
        browser.element('[data-show="error.serverPassError"]').should(be.visible)

    def should_be_opened(self):
        browser.should(have.url(browser.config.base_url + '/login/'))

    def submit(self):
        browser.element('[name="submit"]').click()
