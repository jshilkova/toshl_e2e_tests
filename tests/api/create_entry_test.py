import json
from datetime import datetime

import allure
import jsonschema
import requests

from toshl_finance_demo.data import category
from toshl_finance_demo.data.transaction import EntryType
from utils import api
from utils.load_schema import load_schema
from .conftest import API_URL

@allure.feature('Entry API')
@allure.story('Create entry')
@allure.label('owner', 'allure8')
@allure.tag('smoke', 'regress', 'API')
@allure.label('layer', 'API')
class TestCreateEntry:
    @allure.title('Create income entry')
    @allure.severity('blocker')
    def test_response_success(self, session, remove_all_entries):

        with allure.step("Create entry"):
            resp = session.post(url=f'{API_URL}/api/entries',
                                params={"immediate_update": "true"},
                                json={"amount": 120,
                                      "date": datetime.now().strftime("%Y-%m-%d"),
                                      "currency":
                                          {"code": "GEL"
                                           },
                                      "account": "4346873",
                                      "category": category.grants.id,
                                      "tags": []})

        with allure.step("Validate response status"):
            assert resp.status_code == requests.codes.created

        with allure.step("Validate response content is empty"):
            assert resp.content.decode() == ''


