import pandas as pd
from . import get_info
from time import sleep
from datetime import datetime


class SavingEventInfo:
    def __init__(self, function, eventsId):
        self.function = function
        self.eventsId = eventsId

    def save_event_info(self, function, eventsId):
        data = get_info.GetInfo.get_event_info(eventsId)
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
                place = get_info.GetInfo.get_tk_info(tk_id)

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

            try:
                org_company = event['organizer']['company']['name']
            except Exception:
                org_company = ''

            themes = []
            event_themes = event['themes']
            for theme in event_themes:
                theme_name = get_info.GetInfo.get_theme_name(theme)
                themes.append(theme_name)
                sleep(0.2)

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
                                   'Организация': org_company,
                                   'Статус модерации': moderation,
                                   'Статус публикации': event['status'],
                                   'Темы': ', '.join(themes),
                                   'Теги': [event.get('hashTags')],
                                   'Зарегистрировано пользователей': event['eventStat']['orders'],
                                   'Посетителей': event['eventStat']['visits']}, index=[event['id']])

            all_data = pd.concat([all_data, export])

        all_data.to_excel(writer, sheet_name='Sheet1', index=True, header=True)

        workbook.close()
