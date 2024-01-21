from selene import browser, have


class TransactionDialog:

    def set_amount(self, value):
        browser.element('.amount-input').set_value(value)

    def set_category(self, value):
        browser.element('#addent_category').type(value).press_enter()

    def click_save(self):
        browser.element('[ng-click="savable && onSaveButtonClick()"]').click()

    def set_tag(self, value):
        browser.element('#addent_tags').type(value).press_enter()

    def remove_tag(self, value):
        browser.element('#addent_tags').click()
        browser.all('.presets-tag').element_by(have.exact_text(value)).click()
