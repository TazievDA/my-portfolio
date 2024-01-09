from . import authorization as auth
import requests

class GetInfo:

    @staticmethod
    def search_events(event_name, date_start, date_end, place, moderation):
        token = auth.Auth.get_api_key()
        url = 'https://admin.leader-id.ru/api/v4/admin/events/search'
        headers = {'Authorization': f'Bearer {token}'}
        params = {'paginationSize': 10000}
        if event_name != '':
            q = {'query': event_name}
            params.update(q)
        if date_start != '':
            date_from = {'dateFrom': date_start}
            params.update(date_from)
        if date_end != '':
            date_to = {'dateTo': date_end}
            params.update(date_to)
        if place != '':
            location = {'location': place}
            params.update(location)
        if moderation != '':
            mod = {'moderation': moderation}
            params.update(mod)
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json().get('data', {}).get('_items', {})
            events_id = []
            for event in data:
                id = str(event.get('id'))
                events_id.append(id)
            return events_id
        except Exception:
            print('Мероприятия не найдены.')

    @staticmethod
    def get_event_info(eventsId):
        token = auth.Auth.get_api_key()
        headers = {'Authorization': f'Bearer {token}'}
        responses = []
        for id_ in eventsId:
            url = f'https://leader-id.ru/api/v4/admin/events/{id_}'
            response = requests.get(url, headers=headers)
            try:
                responses.append(response.json()['data'])
            except Exception:
                continue
            print(f'Получаю информацию о мероприятии с ID {id_}')
        return responses

    @staticmethod
    def get_tk_info(tk_id):
        token = auth.Auth.get_api_key()
        headers = {'Authorization': f'Bearer {token}'}
        try:
            url = f'https://leader-id.ru/api/v4/admin/spaces/{tk_id}'
            response = requests.get(url, headers=headers)
            data = response.json()
            return data['data']['name']
        except Exception:
            return f'{tk_id}'

    @staticmethod
    def get_theme_name(theme):
        token = auth.Auth.get_api_key()
        headers = {'Authorization': f'Bearer {token}'}
        try:
            url = f'https://leader-id.ru/api/v4/admin/themes/{theme}'
            response = requests.get(url, headers=headers)
            data = response.json()
            return data['data']['name']
        except KeyError:
            return f'{theme}'

    @staticmethod
    def get_orgs_events(orgs_id):
        events_list = []
        for org_id in orgs_id:
            token = auth.Auth.get_owner_token(org_id)
            api_url = 'https://leader-id.ru/api/v4/owner/events'
            headers = {'Authorization': f'Bearer {token}'}
            params = {'fields': 'id', 'paginationSize': '1000'}
            response = requests.get(api_url, headers=headers, params=params)
            events_id = response.json()['data']['_items']
            for event in events_id:
                events_list.append(str(event['id']))
        return events_list

    @staticmethod
    def get_users_events(userId):
        api_key = auth.Auth.get_api_key()
        params = {'userId': userId, 'paginationSize': '1000'}
        headers = {'Authorization': f'Bearer {api_key}'}
        api_url = 'https://leader-id.ru/api/v4/admin/event-participants/history'
        response = requests.get(api_url, params=params, headers=headers)
        data = response.json()['data']['_items']
        events_list = []
        for event in data:
            events_list.append(event['event']['id'])
        return events_list

    @staticmethod
    def search_companys_events(company_id):
        api_url = f'https://leader-id.ru/api/v4/events/search'
        params = {'organizationId': company_id, 'paginationSize': 999}
        response = requests.get(api_url, params=params)
        data = response.json().get('data', {}).get('_items', {})
        events_id = []
        for event in data:
            events_id.append(event.get('id', ''))
        return events_id

    @staticmethod
    def get_user_info(users_id):
        token = auth.Auth.get_api_key()
        data = []
        headers = {'Authorization': f'Bearer {token}'}
        for user in users_id:
            url = f'https://leader-id.ru/api/v4/admin/users/{user}'
            response = requests.get(url, headers=headers)
            lst = response.json().get('data', {})
            print(f'Получаю информацию о пользователе {lst.get("name", {})}')
            data.append(lst)
            sleep(0.5)
        return data

    @staticmethod
    def get_region(city):
        if '-' in city:
            city = ' '.join(city.split('-'))
        params = {'q': city}
        url = 'https://leader-id.ru/api/v4/cities/search'
        response = requests.get(url, params=params)
        region = response.json().get('data', {})[0].get('region', {})
        return region

    @staticmethod
    def get_participants(events_id):
        token = auth.Auth.get_api_key()
        headers = {'Authorization': f'Bearer {token}'}
        url = 'https://leader-id.ru/api/v4/admin/event-participants/search'
        users_id = []
        for event in events_id:
            params = {'eventId': event, 'paginationSize': 1000}
            response = requests.get(url, headers=headers, params=params)
            data = response.json().get('data', {}).get('_items', {})
            users = []
            for user in data:
                users.append(f'{user["user_id"]}')
            users_id.append(users)
        return zip(events_id, users_id)