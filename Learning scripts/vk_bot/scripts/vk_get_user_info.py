import vk_api
from datetime import date


def get_current_user_info(token, user_id):
    vk = vk_api.VkApi(token=token)
    vk_get_info = vk.method('users.get', {'user_ids': user_id, 'fields': 'bdate, sex, city'})
    birth_date = vk_get_info[0].get('bdate', '')
    if birth_date == '':
        return ('У вас не указана дата рождения. '
                'Для продолжения работы, пожалуйста, укажите дату рождения в вашем профиле.')
    else:
        birth_day = int(birth_date.split('.')[0])
        birth_month = int(birth_date.split('.')[1])
        birth_year = int(birth_date.split('.')[2])
        today = date.today()
        age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))
    city = vk_get_info[0].get('city', '')
    if city == '':
        return 'У вас не выбран город. Для продолжения работы, пожалуйста, укажите город в вашем профиле.'
    else:
        city_id = city.get('id', '')
    sex = vk_get_info[0].get('sex', '')
    if sex == '':
        return 'У вас не указан пол. Для продолжения работы, пожалуйста, укажите пол в вашем профиле.'
    return age, city_id, sex


def get_favorite_user_info(token, user_id):
    vk = vk_api.VkApi(token=token)
    vk_get_info = vk.method('users.get', {'user_ids': user_id, 'fields': 'bdate, sex, city'})
    return vk_get_info
