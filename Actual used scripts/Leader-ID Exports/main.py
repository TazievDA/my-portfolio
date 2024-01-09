from scripts import authorization as auth, get_info as gi, save_users_info as sui, save_event_info as sei, banner as pb
from colorama import Fore, Style
from colorama import just_fix_windows_console
just_fix_windows_console()


def main():
    pb.print_banner()
    while True:
        try:
            function_choice = input('Что будем делать? :)\n1 — получить информацию по мероприятиях\n'
                                    '2 — получить список мероприятий по ID организатора(-ов)\n'
                                    '3 — список участий пользователя в мероприятиях\n'
                                    '4 — список мероприятий организации\n'
                                    '5 — получить данные профиля\n'
                                    '6 — получить данные участников мероприятия(-ий)\n')
            if function_choice == '1':
                export_info = input('Готовимся выгрузить информацию о мероприятиях.'
                                    '\n1 — у меня есть ID нужных мероприятий'
                                    '\n2 — нужно произвести поиск мероприятий'
                                    '\n')
                function_name = 'events info'
                if export_info == '1':
                    events = input('Введите ID мероприятий через запятую: ').split(', ')
                    saving_event_info = sei.SavingEventInfo(function_name, events)
                    saving_event_info.save_event_info(function_name, events)
                    print(Fore.GREEN + 'Файл сохранён в корневую папку')
                if export_info == '2':
                    event_name = ''
                    date_start = ''
                    date_end = ''
                    place = ''
                    moderation = ''
                    while True:
                        filters = input('Выберите фильтры, по которым будем искать:'
                                        '\n1 — название мероприятия;'
                                        '\n2 — дата начала и дата завершения;\n3 — место проведения;'
                                        '\n4 — статус модерации'
                                        '\n')
                        if filters == '1':
                            event_name = input('Введите название мероприятия: ')
                        if filters == '2':
                            date_start = input('Введите дату начала мероприятий в формате 2020-01-31 (ГГГГ-ММ-ДД): ')
                            date_end = input('Введите дату завершения мероприятий в формате 2020-01-31 (ГГГГ-ММ-ДД): ')
                        if filters == '3':
                            place = input('Введите площадку проведения мероприятий: ')
                        if filters == '4':
                            moderation_choice = input('Выберите статус модерации мероприятия:'
                                                      '\n1 — на модерации;'
                                                      '\n2 — одобрено;'
                                                      '\n3 — отклонено'
                                                      '\n')
                            if moderation_choice == '1':
                                moderation = 'wait'
                            if moderation_choice == '2':
                                moderation = 'approved'
                            if moderation_choice == '3':
                                moderation = 'declined'
                        continue_choose_filters = input('Нужно добавить ещё фильтры?\n1 — да;'
                                                        '\n2 — нет'
                                                        '\n')
                        if continue_choose_filters == '2':
                            break
                    getting_info = gi.GetInfo()
                    events = getting_info.search_events(event_name, date_start, date_end, place, moderation)
                    saving_event_info = sei.SavingEventInfo(function_name, events)
                    saving_event_info.save_event_info(function_name, events)
                    print(Fore.GREEN + 'Файл сохранён в корневую папку')

            elif function_choice == '2':
                orgs_id_ = input('Введите ID организаторов через запятую: ').split(', ')
                getting_info = gi.GetInfo()
                if len(orgs_id_) > 1:
                    function_name = f'organizers events'
                else:
                    function_name = f'organizer {orgs_id_[0]} events'
                org_events = getting_info.get_orgs_events(orgs_id_)
                if not org_events:
                    print('У пользователя нет созданных мероприятий.')
                else:
                    saving_event_info = sei.SavingEventInfo(function_name, org_events)
                    saving_event_info.save_event_info(function_name, org_events)
                    print(Fore.GREEN + 'Файл сохранён в корневую папку')

            elif function_choice == '3':
                user_id = int(input('Введите ID пользователя: '))
                function_name = f'user {user_id} participation'
                user_events = gi.GetInfo.get_users_events(userId=user_id)
                if not user_events:
                    print('У пользователя нет посещённых мероприятий.')
                else:
                    saving_event_info = sei.SavingEventInfo(function_name, user_events)
                    saving_event_info.save_event_info(function_name, user_events)
                    print(Fore.GREEN + 'Файл сохранён в корневую папку')
            elif function_choice == '4':
                company_id_ = int(input('Введите ID организации: '))
                getting_info = gi.GetInfo()
                function_name = f'company {company_id_} events'
                company_events = getting_info.search_companys_events(company_id_)
                if not company_events:
                    print('У организации нет мероприятий.')
                else:
                    saving_event_info = sei.SavingEventInfo(function_name, company_events)
                    saving_event_info.save_event_info(function_name, company_events)
                    print(Fore.GREEN + 'Файл сохранён в корневую папку')
            elif function_choice == '5':
                authorization = auth.Auth()
                name = input(
                    'Сейчас вы пытаетесь получить персональные данные пользователей. Пожалуйста, введите ваше ФИО: ')
                print()
                token = input('Введите ваш Bearer токен: ')
                if authorization.pre_auth(token) != 200:
                    print('У вас нет прав для совершения этого действия.')
                    ip = authorization.get_ip()
                    authorization.send_failed_email(name, token, ip)
                    break
                else:
                    print()
                    print('Авторизация прошла успешно. Продолжаем выгружать информацию.')
                    print()
                    ip = authorization.get_ip()
                    authorization.send_success_email(name, token, ip)
                ids = input('Введите ID пользователей через запятую: ').split(', ')
                if len(ids) > 1:
                    function_name = 'users info'
                else:
                    function_name = f'user {ids[0]} info'
                saving_users_info = sui.SavingUsersInfo(function_name, ids)
                saving_users_info.save_user_info(function_name, ids)
                print(Fore.GREEN + 'Файл сохранён в корневую папку')
            elif function_choice == '6':
                authorization = auth.Auth()
                name = input(
                    'Сейчас вы пытаетесь получить персональные данные пользователей. Пожалуйста, введите ваше ФИО: ')
                print()
                token = input('Введите ваш Bearer токен: ')
                if authorization.pre_auth(token) != 200:
                    print('У вас нет прав для совершения этого действия.')
                    ip = authorization.get_ip()
                    authorization.send_failed_email(name, token, ip)
                    break
                else:
                    print()
                    print('Авторизация прошла успешно. Продолжаем выгружать информацию.')
                    print()
                    ip = authorization.get_ip()
                    authorization.send_success_email(name, token, ip)

                getting_info = gi.GetInfo()
                events_id = input('Введите ID мероприятий через запятую: ').split(', ')
                if len(events_id) > 1:
                    function_name = 'participants export'
                else:
                    function_name = f'participants {events_id} export'
                data = getting_info.get_participants(events_id)
                saving_users_info = sui.SavingUsersInfo(function_name, data)
                saving_users_info.save_participants_info(function_name, data)
        except Exception:
            print(Fore.RED + 'Ошибка.' + Fore.RESET)
        close_app = input('Введите' + Fore.CYAN + ' любой символ ' + Style.RESET_ALL + 'для продолжения или нажмите' +
                          Fore.CYAN + ' Enter ' + Style.RESET_ALL + 'для выхода.')
        if close_app == '':
            break
        else:
            print()


if __name__ == '__main__':
    main()
