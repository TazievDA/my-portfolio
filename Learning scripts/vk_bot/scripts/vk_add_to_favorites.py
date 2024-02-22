from random import randrange

from data_base.insert_database import add_favorite, add_top3
from data_base.select_database import select_current_user, select_one_favorite
from scripts.keyboard_main import keyboard_main


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
