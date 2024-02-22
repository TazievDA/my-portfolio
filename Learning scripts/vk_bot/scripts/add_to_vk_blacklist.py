from random import randrange

from data_base.insert_database import add_blacklist
from data_base.select_database import select_current_user
from scripts.keyboard_main import keyboard_main


def add_to_vk_blacklist(user_id, vk, vk_id):
    botusers_id = select_current_user(user_id)
    add_blacklist(botusers_id, vk_id)
    return vk.method('messages.send', {'user_id': user_id, 'message': 'Пользователь добавлен в чёрный список.',
                                       'random_id': randrange(10 ** 7),
                                       'keyboard': keyboard_main()})
