from selene import browser


class ConfirmationDialog:
    def confirm_delete(self):
        browser.element('.modal-dialog [ng-click^="onDelete"]').click()
