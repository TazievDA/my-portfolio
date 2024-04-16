import requests


def search_organization(api_url, name, api_key):
    headers = {'Authorization': f'Bearer {api_key}'}
    params = {'name': name, 'paginationSize': 1000}
    response = requests.get(api_url, params=params, headers=headers)
    return response