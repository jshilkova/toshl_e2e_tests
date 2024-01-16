from selene import browser, have


class TransactionDetails:


    def click_edit_button(self):
        browser.element('[ng-click="onEdit()"]').click()

    def click_duplicate_button(self):
        browser.element('[ng-click="onDuplicate()"]').click()

    def click_delete_button(self):
        browser.element('[ng-click="onDelete()"]').click()

    def should_have_amount(self, amount):
        browser.element('.entry-details_amount').should(have.text(amount))

    def should_have_category(self, category_name):
        browser.element('[ng-bind="item.category"]').should(have.text(category_name))

    def should_have_tag(self, tag_name):
        browser.element('[ng-bind="item.tags"]').should(have.text(tag_name))

    def should_not_have_tags(self):
        browser.all('.min-col6').should(have.size(3))


