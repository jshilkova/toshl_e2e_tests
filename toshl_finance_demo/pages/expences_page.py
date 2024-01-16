from selene import browser


class ExpensesPage:
    def open_or_refresh(self):
        url = '/app/#/expenses'
        if browser.driver.current_url.endswith(url):
            browser.driver.refresh()
        else:
            browser.open(url)
