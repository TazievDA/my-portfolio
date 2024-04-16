import pytest
from ..scripts.search_organization import search_organization
from ..scripts.get_api_key import get_api_key


def test_correct_search():
    api_url = 'https://admin.leader-id.ru/api/v4/admin/organizations'
    api_key = get_api_key()
    expected = 'tests'
    actual = search_organization(api_url, expected, api_key).json().get('data', {}).get('_items', {})
    assert expected in actual[0].get('name', '').lower()
    assert expected in actual[len(actual) - 1].get('name', '').lower()

def test_no_orgs():
    api_url = 'https://admin.leader-id.ru/api/v4/admin/organizations'
    api_key = get_api_key()
    expected = 0
    actual = search_organization(api_url, "tests%67&%^", api_key).json().get('data', {}).get('_items', {})
    assert expected == len(actual)

def test_wrong_url():
    api_url = 'https://admin.leader-id.ru/api/v4/admin/organizations1'
    api_key = get_api_key()
    expected = 200
    actual = search_organization(api_url, "tests", api_key).status_code
    assert actual != expected