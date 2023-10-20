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

    api_url = 'https://admin.leader-id.ru/api/v4/admin/organizations'

    while True:
        organization_name = input("Введите название организации для поиска: ")

        search_result = search_organization(api_url, organization_name, api_key)

        if ('data' not in search_result or '_items' not in search_result['data']
                or not all('id' in org for org in search_result['data']['_items'])):
            print(Fore.RED + "Результаты поиска организации некорректны." + Style.RESET_ALL)
            continue

        orgs_to_merge = search_result['data']['_items']

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

        selected_orgs_input = input("Введите номера организаций для удаления через запятую "
                                    "(или '0' чтобы пропустить шаг удаления): ")

        if selected_orgs_input.strip() != "0":
            try:
                selected_orgs = set(int(idx) for idx in selected_orgs_input.split(","))
            except ValueError:
                print(Fore.RED + "Ошибка: Некорректный ввод номеров организаций." + Style.RESET_ALL)
                continue

            orgs_to_merge = [org for idx, org in enumerate(orgs_to_merge, start=1) if idx not in selected_orgs]

            print(Fore.YELLOW + "Организации для объединения после удаления:")
            table = PrettyTable()
            table.field_names = ["#", "ID", "Name"]
            for idx, org in enumerate(orgs_to_merge, start=1):
                table.add_row([idx, org['id'], org['name']])
            print(table)
            print(Style.RESET_ALL)

        if len(orgs_to_merge) < 2:
            print(Fore.RED + "Недостаточно организаций для объединения." + Style.RESET_ALL)
            continue

        confirmation = input("Подтвердите объединение организаций? (да/нет): ")
        if confirmation.lower() != 'да':
            continue

        org_ids_to_merge = [org['id'] for org in orgs_to_merge]

        preferred_org_id = input("Введите ID предпочитаемой организации для объединения: ")

        try:
            preferred_org_id = int(preferred_org_id)
        except ValueError:
            print(Fore.RED + "Ошибка: Некорректный ID предпочитаемой организации." + Style.RESET_ALL)
            continue

        for org_id in org_ids_to_merge:
            merge_result = merge_organizations('https://leader-id.ru/api/v4/admin/organizations/merge', [org_id],
                                               preferred_org_id, api_key)

            if merge_result.get('status') == 'error':
                print(Fore.RED + f"Ошибка при объединении организации с ID {org_id}: {merge_result.get('message')}" +
                      Style.RESET_ALL)
            else:
                print(Fore.GREEN + f"Организация с ID {org_id} успешно объединена.")
            print(Style.RESET_ALL)

        print(Fore.GREEN + "Все организации успешно объединены." + Style.RESET_ALL)

        choice = input("Хотите выполнить еще одно объединение организаций? (да/нет): ")
        if choice.lower() != 'да':
            break


if __name__ == "__main__":
    main()
