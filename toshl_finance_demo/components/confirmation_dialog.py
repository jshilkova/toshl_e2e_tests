from selene import browser, have


class ConfirmationDialog:
    def confirm_delete(self):
        browser.element('.modal-dialog [ng-click^="onDelete"]').click()

