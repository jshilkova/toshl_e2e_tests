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


class TestCreateEntry:
    def test_success(self, session, remove_all_entries):

        with allure.step("Create entry"):
            api.add_entry(session, EntryType.EXPENSE, category.education.id, 120)
            entries = api.get_all_entries(session)

        with allure.step("Delete entry"):
            resp = session.delete(url=f'{API_URL}/api/entries/{entries[0]["id"]}')

        with allure.step("Validate response status"):
            assert resp.status_code == requests.codes.no_content

        with allure.step("Validate response content is empty"):
            assert resp.content.decode() == ''

    def test_failed_not_existing(self, session, remove_all_entries):
        not_existing_id = "1"
        with allure.step("Delete entry"):
            resp = session.delete(url=f'{API_URL}/api/entries/{not_existing_id}')

        with allure.step("Validate response status is 404"):
            assert resp.status_code == requests.codes.not_found

        with allure.step("Validate response content is empty"):
            assert resp.json()['description'] == f'Object with id {not_existing_id} not found.'


