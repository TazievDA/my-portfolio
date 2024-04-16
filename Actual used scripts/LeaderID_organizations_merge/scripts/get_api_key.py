import requests
import os


def get_api_key():
    api_url = 'https://leader-id.ru/api/v4/auth/refresh-token'
    data = {
        'refreshToken': os.getenv('REFRESH_TOKEN'),
    }
    refresh_response = requests.post(api_url, json=data)
    api_key = refresh_response.json()['data']['access_token']
    return api_key