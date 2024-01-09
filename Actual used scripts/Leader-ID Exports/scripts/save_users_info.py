import pandas as pd
from . import get_info
from datetime import datetime


class SavingUsersInfo():
    def __init__(self, function, usersId):
        self.function = function
        self.usersId = usersId

    def save_user_info(self, function, users_id):
        data = get_info.GetInfo.get_user_info(users_id)
        date = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

        writer = pd.ExcelWriter(f'{function} {date}.xlsx', engine='xlsxwriter')

        workbook = writer.book

        all_data = pd.DataFrame()

        for idx, user in enumerate(data):
            try:
                try:
                    city = user.get('address', {})
                    region = get_info.GetInfo.get_region(city)
                except Exception:
                    city = ''
                    region = ''
                # if user.get('employment')
                print(f'Формирую выгрузку для пользователя "{user["name"]}"')
                export = pd.DataFrame({'ФИО': user.get('name', {}), 'Дата рождения': user.get('birthday', {}),
                                       'Электронная почта': user.get('email', {}), 'Номер телефона': user.get('phone', {}),
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

    def save_participants_info(self, function, datas):
        date = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
        all_data = pd.DataFrame()
        writer = pd.ExcelWriter(f'{function} {date}.xlsx', engine='xlsxwriter')
        workbook = writer.book

        for event, users_id in datas:
            data = get_info.GetInfo.get_user_info(users_id)
            for user in data:
                try:
                    try:
                        city = user.get('address', {})
                        region = get_info.GetInfo.get_region(city)
                    except Exception:
                        city = ''
                        region = ''
                    print(f'Формирую выгрузку для пользователя "{user["name"]}"')
                    export = pd.DataFrame({'ID': user['id'], 'ФИО': user.get('name', {}), 'Дата рождения': user.get('birthday', {}),
                                           'Электронная почта': user.get('email', {}), 'Номер телефона': user.get('phone', {}),
                                           'Место работы': user.get('employment', {}).get('company', None),
                                           'Должность': user.get('employment', {}).get('position', None),
                                           'Роль': user.get('roleName', {}),
                                           'Город проживания': city, 'Регион': region, 'Статус': user.get('status', {})},
                                          index=[event])
                    all_data = pd.concat([all_data, export])
                except Exception:
                    export = pd.DataFrame({'ID': user['id'], 'ФИО': '', 'Дата рождения': '',
                                           'Электронная почта': '', 'Номер телефона': '',
                                           'Место работы': '',
                                           'Должность': '',
                                           'Роль': '',
                                           'Город проживания': '', 'Регион': '', 'Статус': ''},
                                          index=[event])
                    all_data = pd.concat([all_data, export])
                    continue

        all_data.to_excel(writer, sheet_name='Sheet1', index=True, header=True)

        workbook.close()
