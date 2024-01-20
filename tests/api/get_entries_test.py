from datetime import datetime
import allure
import jsonschema
import requests
from config import API_URL
from toshl_finance_demo.data import category
from toshl_finance_demo.data.transaction import EntryType

from toshl_finance_demo.utils.load_schema import load_schema
from toshl_finance_demo.utils import api


@allure.feature('Entry API')
@allure.story('Get entries')
@allure.label('owner', 'allure8')
@allure.tag('smoke', 'regress', 'API')
@allure.label('layer', 'API')
class TestGetEntries:
    @allure.title('Get entries')
    @allure.severity('critical')
    def test_response_success(self, session, remove_all_entries):
        api.add_entry(session, EntryType.EXPENSE, category.education.id, 120)
        api.add_entry(session, EntryType.EXPENSE, category.charity.id, 140)

        with allure.step("Get entries"):
            resp = session.get(url=f'{API_URL}/api/entries/',
                               params={"from": "2024-01-01", "to": datetime.now().strftime("%Y-%m-%d")})
            entries = resp.json()
        with allure.step("Validate response status"):
            assert resp.status_code == requests.codes.ok

        with allure.step("Validate response schema"):
            schema = load_schema("get_entries.json")
            jsonschema.validate(entries, schema)

        with allure.step("Validate response content"):
            assert len(entries) == 2
            entries.sort(key=lambda e: e["id"])
            assert entries[0]['amount'] == -120
            assert entries[1]['amount'] == -140

            assert entries[0]['category'] == str(category.education.id)
            assert entries[1]['category'] == str(category.charity.id)

            assert entries[0]['currency']['code'] == 'GEL'
            assert entries[1]['currency']['code'] == 'GEL'

    @allure.title('Get empty entries list')
    @allure.severity('minor')
    def test_empty_response(self, session, remove_all_entries):

        with allure.step("Get entries"):
            resp = session.get(url=f'{API_URL}/api/entries/',
                               params={"from": "2024-01-01", "to": datetime.now().strftime("%Y-%m-%d")})

        with allure.step("Validate response status"):
            assert resp.status_code == requests.codes.ok

        with allure.step("check that response is empty"):
            assert len(resp.json()) == 0