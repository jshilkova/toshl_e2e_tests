from datetime import datetime
import allure
import requests
from toshl_finance_demo_test.data import category
from config import API_URL
from toshl_finance_demo_test.data.user import test_user


@allure.feature('Entry API')
@allure.story('Create entry')
@allure.label('owner', 'allure8')
@allure.tag('smoke', 'regress', 'API')
@allure.label('layer', 'API')
class TestCreateEntry:
    @allure.title('Create income entry')
    @allure.severity('blocker')
    def test_create_income_success(self, session, remove_all_entries):
        with allure.step("Create entry"):
            resp = session.post(url=f'{API_URL}/api/entries',
                                params={"immediate_update": "true"},
                                json={"amount": 120,
                                      "date": datetime.now().strftime("%Y-%m-%d"),
                                      "currency":
                                          {"code": "GEL"
                                           },
                                      "account": test_user.account,
                                      "category": category.grants.id,
                                      "tags": []})

        with allure.step("Validate response status"):
            assert resp.status_code == requests.codes.created

        with allure.step("Validate response content is empty"):
            assert resp.content.decode() == ''
