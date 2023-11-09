import requests
import openpyxl
import pandas as pd
import xlsxwriter
import json
import smtplib
import http.client
from time import sleep
from colorama import Fore, Style
from colorama import just_fix_windows_console
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header

just_fix_windows_console()


def print_banner():
    banner = r"""

    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒▒░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒
    ▒▒▒▒▒░░░░░▒▒▒░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒
    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

   Leader-ID Support Team.
   Утилита для выгрузок.
    """

    print(Fore.CYAN + banner + Style.RESET_ALL)


class Auth:
    @staticmethod
    def pre_auth(token):
        headers = {'Authorization': f'Bearer {token}'}
        params = {'id': 292338}
        url = 'https://leader-id.ru/api/v4/admin/users'
        response = requests.get(url, params=params, headers=headers)
        return response.status_code

    @staticmethod
    def send_email(name, token, ip):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('xxxxx@xxxx.com', 'password')
        message = MIMEText(f'IP: {ip} {name} с токеном {token} только что запросил выгрузку данных пользователей через '
                           f'Leader-ID Export.', 'plain', 'utf-8')
        message['Subject'] = Header('Выгрузка контактных данных', 'utf-8')
        smtpObj.sendmail('from_email@xxxx.com', 'to_email@xxxx.com', message.as_string())

    @staticmethod
    def get_ip():
        conn = http.client.HTTPConnection("ifconfig.me")
        conn.request("GET", "/ip")
        return conn.getresponse().read()

    @staticmethod
    def get_api_key() -> object:
        api_url = 'https://leader-id.ru/api/v4/auth/refresh-token'
        data = {
            'refreshToken': 'refresh_token'
        }
        refresh_response = requests.post(api_url, json=data)
        api_key = refresh_response.json()['data']['access_token']
        return api_key

    @staticmethod
    def get_owner_token(org_id):
        api_key = Auth.get_api_key()
        api_url = 'https://leader-id.ru/api/v4/admin/users/auth'
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
        data = json.dumps({
            'userId': org_id
        })

        token_response = requests.post(api_url, headers=headers, data=data)
        token = token_response.json()['data']['token']
        return token


class GetInfo:

    @staticmethod
    def get_event_info(eventsId):
        token = Auth.get_api_key()
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
        token = Auth.get_api_key()
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
        token = Auth.get_api_key()
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
            token = Auth.get_owner_token(org_id)
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
        api_key = Auth.get_api_key()
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
        token = Auth.get_api_key()
        data = []
        headers = {'Authorization': f'Bearer {token}'}
        for user in users_id:
            url = f'https://leader-id.ru/api/v4/admin/users/{user}'
            response = requests.get(url, headers=headers)
            lst = response.json().get('data', {})
            print(f'Получаю информацию о пользователе {lst.get("name", {})}')
            data.append(lst)
            sleep(0.2)
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


class SavingEventInfo:
    def __init__(self, function, eventsId):
        self.function = function
        self.eventsId = eventsId

    def save_json_to_excel(self, function, eventsId):
        data = GetInfo.get_event_info(eventsId)
        date = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

        writer = pd.ExcelWriter(f'{function} {date}.xlsx', engine='xlsxwriter')

        workbook = writer.book

        all_data = pd.DataFrame()

        for event in data:
            info = event['info']
            try:
                info_dict = eval(info)
                event_info_list = []
                for idx in info_dict['blocks']:
                    event_info_list.append(idx['data']['text'])
                event_info = '\n'.join(event_info_list)
            except Exception:
                event_info = ''

            live_links = [event.get('live')]
            if not live_links:
                live_links = 'Нет'

            if event['format'] != 'space':
                if event['place']:
                    place = f"{event['place']['address']}, {event['place']['name']}"
                else:
                    place = ''
            else:
                tk_id = event['space']['spaceId']
                place = GetInfo.get_tk_info(tk_id)

            type_of_place = ''
            if event['format'] == 'space':
                type_of_place = 'В Точке кипения'
            elif event['format'] == 'online':
                type_of_place = 'Онлайн'
            elif event['format'] == 'online' and event['space']:
                type_of_place = 'Онлайн при поддержке Точки кипения'
            elif event['format'] == 'place':
                type_of_place = 'Не в Точке кипения'

            try:
                org_name = event['organizer']['name']
                org_phone = event['organizer']['phone']
                org_email = event['organizer']['email']
            except Exception:
                org_name = ''
                org_phone = ''
                org_email = ''

            themes = []
            event_themes = event['themes']
            for theme in event_themes:
                theme_name = GetInfo.get_theme_name(theme)
                themes.append(theme_name)

            participation_format = ''
            if event['participationFormat'] == 'person':
                participation_format = 'Индивидуальное'
            elif event['participationFormat'] == 'team':
                participation_format = 'Командное'
            elif event['participationFormat'] == 'quiz':
                participation_format = 'Опрос'

            if event['moderation'] == 'declined':
                moderation = 'Отклонено'
            elif event['moderation'] == 'approved':
                moderation = 'Одобрено'
            elif event['moderation'] == 'wait':
                moderation = 'На модерации'
            else:
                moderation = 'Черновик'

            print(f'Формирую выгрузку для мероприятия "{event["name"]}"')

            export = pd.DataFrame({'Название': event['name'], 'Создатель': event['createdBy'], 'Описание': event_info,
                                   'Ссылка на трансляцию': live_links, 'Дата создания': event['createdAt'],
                                   'Дата модерации': event['moderatedAt'], 'ID модератора': event['moderatedBy'],
                                   'Дата старта мероприятия': event['dateStart'],
                                   'Дата завершения мероприятия': event['dateEnd'],
                                   'Тип участия': participation_format,
                                   'Формат проведения': type_of_place, 'Место проведения': place,
                                   'ФИО организатора': org_name,
                                   'Номер телефона организатора': org_phone,
                                   'Электронная почта организатора': org_email,
                                   'Статус модерации': moderation,
                                   'Статус публикации': event['status'],
                                   'Темы': ', '.join(themes),
                                   'Зарегистрировано пользователей': event['eventStat']['orders'],
                                   'Посетителей': event['eventStat']['visits']}, index=[event['id']])

            all_data = pd.concat([all_data, export])

        all_data.to_excel(writer, sheet_name='Sheet1', index=True, header=True)

        workbook.close()


class SavingUsersInfo:
    def __init__(self, function, usersId):
        self.function = function
        self.usersId = usersId

    def save_user_info(self, function, users_id):
        data = GetInfo.get_user_info(users_id)
        date = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

        writer = pd.ExcelWriter(f'{function} {date}.xlsx', engine='xlsxwriter')

        workbook = writer.book

        all_data = pd.DataFrame()

        for idx, user in enumerate(data):
            try:
                city = user.get('address', {})
                region = GetInfo.get_region(city)
                # if user.get('employment')
                print(f'Формирую выгрузку для пользователя "{user["name"]}"')
                export = pd.DataFrame({'ФИО': user.get('name', {}), 'Дата рождения': user.get('birthday', {}),
                                       'Электронная почта': user.get('email', {}),
                                       'Номер телефона': user.get('phone', {}),
                                       'Место работы': user.get('employment', {}).get('company', None),
                                       'Должность': user.get('employment', {}).get('position', None),
                                       'Роль': user.get('roleName', {}),
                                       'Город проживания': city, 'Регион': region, 'Статус': user.get('status', {})},
                                      index=[user['id']])
                all_data = pd.concat([all_data, export])
            except Exception:
                export = pd.DataFrame({'ФИО': '', 'Дата рождения': '',
                                       'Электронная почта': '', 'Номер телефона': '',
                                       'Место работы': '',
                                       'Должность': '',
                                       'Роль': '',
                                       'Город проживания': '', 'Регион': '', 'Статус': ''},
                                      index=[users_id[idx]])
                all_data = pd.concat([all_data, export])
                continue

        all_data.to_excel(writer, sheet_name='Sheet1', index=True, header=True)

        workbook.close()


def main():
    print_banner()
    while True:
        try:
            function_choice = input('Что будем делать? :)\n1 — получить информацию по ID мероприятий\n'
                                    '2 — получить список мероприятий по ID организатора(-ов)\n'
                                    '3 — список участий пользователя в мероприятиях\n'
                                    '4 — список мероприятий организации\n'
                                    '5 — получить данные профиля\n')
            if function_choice == '1':
                function_name = 'events info'
                events = input('Введите ID мероприятий через запятую: ').split(', ')
                saving_event_info = SavingEventInfo(function_name, events)
                saving_event_info.save_json_to_excel(function_name, events)
                print(Fore.GREEN + 'Файл сохранён в корневую папку')

            elif function_choice == '2':
                orgs_id_ = input('Введите ID организаторов через запятую: ').split(', ')
                getting_info = GetInfo()
                if len(orgs_id_) > 1:
                    function_name = f'organizers events'
                else:
                    function_name = f'organizer {orgs_id_[0]} events'
                org_events = getting_info.get_orgs_events(orgs_id_)
                if not org_events:
                    print('У пользователя нет созданных мероприятий.')
                else:
                    saving_event_info = SavingEventInfo(function_name, org_events)
                    saving_event_info.save_json_to_excel(function_name, org_events)
                    print(Fore.GREEN + 'Файл сохранён в корневую папку')

            elif function_choice == '3':
                user_id = int(input('Введите ID пользователя: '))
                function_name = f'user {user_id} participation'
                user_events = GetInfo.get_users_events(userId=user_id)
                if not user_events:
                    print('У пользователя нет посещённых мероприятий.')
                else:
                    saving_event_info = SavingEventInfo(function_name, user_events)
                    saving_event_info.save_json_to_excel(function_name, user_events)
                    print(Fore.GREEN + 'Файл сохранён в корневую папку')
            elif function_choice == '4':
                company_id_ = int(input('Введите ID организации: '))
                getting_info = GetInfo()
                function_name = f'company {company_id_} events'
                company_events = getting_info.search_companys_events(company_id_)
                if not company_events:
                    print('У организации нет мероприятий.')
                else:
                    saving_event_info = SavingEventInfo(function_name, company_events)
                    saving_event_info.save_json_to_excel(function_name, company_events)
                    print(Fore.GREEN + 'Файл сохранён в корневую папку')
            elif function_choice == '5':
                authorization = Auth()
                name = input(
                    'Сейчас вы пытаетесь получить персональные данные пользователей. Пожалуйста, введите ваше ФИО: ')
                print()
                token = input('Введите ваш Bearer токен: ')
                if authorization.pre_auth(token) != 200:
                    print('У вас нет прав для совершения этого действия.')
                    ip = authorization.get_ip()
                    authorization.send_email(name, token, ip)
                    break
                else:
                    print()
                    print('Авторизация прошла успешно. Продолжаем выгружать информацию.')
                    print()
                    ip = authorization.get_ip()
                    authorization.send_email(name, token, ip)
                ids = input('Введите ID пользователей через запятую: ').split(', ')
                if len(ids) > 1:
                    function_name = 'users info'
                else:
                    function_name = f'user {ids[0]} info'
                saving_users_info = SavingUsersInfo(function_name, ids)
                saving_users_info.save_user_info(function_name, ids)
                print(Fore.GREEN + 'Файл сохранён в корневую папку')

        except Exception:
            print(Fore.RED + 'Ошибка.')

        print(Style.RESET_ALL)
        close_app = input('Введите' + Fore.CYAN + ' любой символ ' + Style.RESET_ALL + 'для продолжения или нажмите' +
                          Fore.CYAN + ' Enter ' + Style.RESET_ALL + 'для выхода.')
        if close_app == '':
            break
        else:
            print()


if __name__ == '__main__':
    main()
