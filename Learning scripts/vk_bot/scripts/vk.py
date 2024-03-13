import vk_api

from random import randrange

from datetime import date

from data_base.insert import add_blacklist,add_favorite, add_top3
from data_base.select import select_current_user, select_one_favorite

from scripts.keyboard import keyboard_main


def add_to_vk_blacklist(user_id, vk, vk_id):
    botusers_id = select_current_user(user_id)
    add_blacklist(botusers_id, vk_id)
    return vk.method('messages.send', {'user_id': user_id, 'message': 'Пользователь добавлен в чёрный список.',
                                       'random_id': randrange(10 ** 7),
                                       'keyboard': keyboard_main()})


def add_to_vk_favorites(user_id, vk, vk_id, message, attachments):
    botusers_id = select_current_user(user_id)
    favorite = select_one_favorite(user_id, vk_id)
    if favorite is not None:
        return vk.method('messages.send', {'user_id': user_id, 'message': 'Пользователь уже есть в избранном',
                                           'random_id': randrange(10 ** 7),
                                           'keyboard': keyboard_main()})
    else:
        user_info = message.split(' ')  # получаем name, link и surname пользователя
        name = user_info[0]
        surname = user_info[1]
        link = user_info[2]
        add_favorite(botusers_id, vk_id, link, name, surname)
        added_favorite = select_one_favorite(user_id, vk_id)
        favourites_id = added_favorite.id
        add_top3(favourites_id, attachments)
        return vk.method('messages.send', {'user_id': user_id, 'message': 'Пользователь добавлен в избранное.',
                                           'random_id': randrange(10 ** 7),
                                           'keyboard': keyboard_main()})


def get_user_photos(personal_token, search_id):
    vk = vk_api.VkApi(token=personal_token)
    try:
        photos = vk.method('photos.get', {'owner_id': search_id, 'album_id': 'profile', 'extended': 1})
        return photos.get('items')
    except vk_api.exceptions.VkApiError:
        return []


def get_top_photos_by_likes(personal_token, search_id):
    photos = get_user_photos(personal_token, search_id)
    photos.sort(key=lambda x: x.get('likes', {}).get('count'), reverse=True)
    return photos[0:3]


def get_photos_links(personal_token, search_id):
    photos = get_top_photos_by_likes(personal_token, search_id)
    links = []
    ids = []
    for photo in photos:
        links.append(photo.get('sizes')[-1].get('url'))
        ids.append(photo.get('id'))
    return list(zip(links, ids))


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
