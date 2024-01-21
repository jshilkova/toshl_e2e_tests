from selene import browser, have


class LeftPanel:

    def verify_user(self, name):
        (browser.element('[ng-bind-html="viewData.titles.userDisplayName"]')
         .with_(timeout=10).should(have.exact_text(name)))
