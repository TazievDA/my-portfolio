import requests
from prettytable import PrettyTable
from colorama import Fore, Style
from colorama import just_fix_windows_console
just_fix_windows_console()


def search_organization(api_url, name, api_key):
    headers = {'Authorization': f'Bearer {api_key}'}
    params = {'name': name, 'paginationSize': 1000}
    response = requests.get(api_url, params=params, headers=headers)
    return response.json()


def merge_organizations(api_url, org_ids, preferred_org_id, api_key):
    if preferred_org_id in org_ids:
        org_ids.remove(preferred_org_id)
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {
        'orgIds': org_ids,
        'preferredOrgId': preferred_org_id
    }
    response = requests.post(api_url, json=data, headers=headers)
    return response.json()


def get_api_key():
    api_url = 'https://leader-id.ru/api/v4/auth/refresh-token'
    data = {
        'refreshToken': 'refresh_token'
    }
    refresh_response = requests.post(api_url, json=data)
    api_key = refresh_response.json()['data']['access_token']
    return api_key


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
   Объединение организаций
    """

    print(Fore.CYAN + banner + Style.RESET_ALL)


def main():

    print_banner()

    api_key = get_api_key()

    # Замените эту переменную своим значением API URL.
    api_url = 'https://admin.leader-id.ru/api/v4/admin/organizations'

    while True:
        # Запросим у пользователя ввод названия организации.
        organization_name = input("Введите название организации для поиска: ")

        # Произведем поиск организации по введенному названию.
        search_result = search_organization(api_url, organization_name, api_key)

        # Проверяем, есть ли результаты поиска и есть ли поле 'id' в каждой организации.
        if 'data' not in search_result or '_items' not in search_result['data'] or not all('id' in org for org in search_result['data']['_items']):
            print(Fore.RED + "Результаты поиска организации некорректны." + Style.RESET_ALL)
            continue

        # Получаем список организаций из результатов поиска.
        orgs_to_merge = search_result['data']['_items']

        # Проверяем, есть ли хотя бы две организации для объединения.
        if len(orgs_to_merge) < 2:
            print(Fore.RED + "Недостаточно организаций для объединения." + Style.RESET_ALL)
            continue

        print(Fore.YELLOW + "Организации для объединения:")
        table = PrettyTable()
        table.field_names = ["#", "ID", "Name"]
        for idx, org in enumerate(orgs_to_merge, start=1):
            table.add_row([idx, org['id'], org['name']])
        print(table)
        print(Style.RESET_ALL)

        # Запрашиваем у пользователя ввод номеров организаций, которые нужно удалить (через запятую).
        selected_orgs_input = input("Введите номера организаций для удаления через запятую "
                                    "(или '0' чтобы пропустить шаг удаления): ")

        # Обработка введенных номеров организаций для удаления.
        if selected_orgs_input.strip() != "0":
            selected_orgs = set()
            try:
                selected_orgs = set(int(idx) for idx in selected_orgs_input.split(","))
            except ValueError:
                print(Fore.RED + "Ошибка: Некорректный ввод номеров организаций." + Style.RESET_ALL)
                continue

            orgs_to_merge = [org for idx, org in enumerate(orgs_to_merge, start=1) if idx not in selected_orgs]

            # Выводим информацию об оставшихся организациях для объединения.
            print(Fore.YELLOW + "Организации для объединения после удаления:")
            table = PrettyTable()
            table.field_names = ["#", "ID", "Name"]
            for idx, org in enumerate(orgs_to_merge, start=1):
                table.add_row([idx, org['id'], org['name']])
            print(table)
            print(Style.RESET_ALL)

        # Проверяем, осталось ли хотя бы две организации для объединения.
        if len(orgs_to_merge) < 2:
            print(Fore.RED + "Недостаточно организаций для объединения." + Style.RESET_ALL)
            continue

        # Запрашиваем подтверждение пользователя перед объединением.
        confirmation = input("Подтвердите объединение организаций? (да/нет): ")
        if confirmation.lower() != 'да':
            continue

        # Запрашиваем у пользователя ввод preferred_org_id.
        preferred_org_id = input("Введите ID предпочитаемой организации для объединения: ")

        try:
            preferred_org_id = int(preferred_org_id)
        except ValueError:
            print(Fore.RED + "Ошибка: Некорректный ID предпочитаемой организации." + Style.RESET_ALL)
            continue

        # Получаем список ID организаций для объединения.
        org_ids_to_merge = [org['id'] for org in orgs_to_merge if org['id'] != preferred_org_id]

        # Объединяем организации по 1 элементу за раз.
        results = []
        count = 0
        for org_id in org_ids_to_merge:
            merge_result = merge_organizations('https://leader-id.ru/api/v4/admin/organizations/merge', [org_id], preferred_org_id, api_key)

            if merge_result.get('errors'):
                results.append(merge_result.get('errors'))
                count += 1
                print(Fore.RED + f"Ошибка при объединении организации с ID {org_id}: {merge_result.get('errors')}" + Style.RESET_ALL)
            else:
                print(Fore.GREEN + f"Организация с ID {org_id} успешно объединена.")
            print(Style.RESET_ALL)

        if not results:
            print(Fore.GREEN + "Все организации успешно объединены." + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"Ошибок при объединении организаций: {count}" + Style.RESET_ALL)

        # Запрашиваем у пользователя, хочет ли он выполнить еще одно объединение.
        choice = input("Хотите выполнить еще одно объединение организаций? (да/нет): ")
        if choice.lower() != 'да':
            break


if __name__ == "__main__":
    main()
