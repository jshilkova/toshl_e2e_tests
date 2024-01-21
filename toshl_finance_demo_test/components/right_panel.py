from selene import browser, have


class RightPanel:

    def click_add_button(self):
        browser.element('[ng-click="addEntry(central.type)"]').click()

    def click_expense(self, amount):
        browser.with_(timeout=10).all('.categoriesListItem').element_by(have.text(amount)).click()

    def record_should_present(self, category_name, amount):
        (browser.all('.categoriesListItem').element_by(have.text(category_name))
         .element('.categoriesListItem-amount').should(have.text(amount)))

    def should_have_records_count(self, count):
        browser.all('.categoriesListItem').should(have.size(count))
