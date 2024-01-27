from datetime import datetime

import allure
from requests import Session

from config import API_URL
from toshl_finance_demo_test.data.transaction import EntryType
from toshl_finance_demo_test.data.user import test_user


def add_entry(session: Session, entry_type: EntryType, category_id: str, amount: int, tag_ids=None):
    if entry_type == EntryType.EXPENSE:
        amount = -amount

    if tag_ids is None:
        tag_ids = []
    else:
        tag_ids = [','.join(tag_ids)]
    with allure.step("Add expense with API"):
        session.post(url=f'{API_URL}/api/entries',
                     params={"immediate_update": "true"},
                     json={"amount": amount,
                           "date": datetime.now().strftime("%Y-%m-%d"),
                           "currency":
                               {"code": "GEL"
                                },
                           "account": test_user.account,
                           "category": category_id,
                           "tags": tag_ids})


def get_all_entries(session: Session):
    resp = session.get(url=f'{API_URL}/api/entries/',
                       params={"from": "2024-01-01", "to": datetime.now().strftime("%Y-%m-%d")})
    return resp.json()
