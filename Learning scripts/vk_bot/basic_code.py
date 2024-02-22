from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from data_base.insert_database import add_bot_users, Base, engine
from data_base.select_database import select_all_favorites, check_current_user
from scripts.add_to_vk_blacklist import add_to_vk_blacklist
from scripts.keyboard_main import keyboard_main
from scripts.return_message import return_message, return_favorites_list
from scripts.search_users import search_users
from scripts.vk_add_to_favorites import add_to_vk_favorites
from scripts.vk_get_user_info import get_current_user_info

community_token = input('Community token: ')
personal_token = input('Personal token: ')

vk = vk_api.VkApi(token=community_token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),
                                'keyboard': keyboard_main()})


Base.metadata.create_all(engine)

counter = 0

vk_id = int()
attachments = []
message = ''

search_result = None
ids = None

age = None
city_id = None
sex = None

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            if age is None and city_id is None and sex is None:
                age, city_id, sex = get_current_user_info(community_token, event.user_id)

            if check_current_user(event.user_id) is None:
                add_bot_users(event.user_id, city_id, age, sex)

            if request == "Привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")

            elif request == "Найди мне пару":
                write_msg(event.user_id, 'Ищем подходящих пользователей.')
                if search_result is None and ids is None:
                    search_result, ids = search_users(personal_token, age, city_id, sex, event.user_id)
                result, vk_id, attachments, message = return_message(personal_token, vk, event, counter, event.user_id,
                                                                     search_result, ids)

            elif request == 'Покажи ещё':
                counter += 1
                result, vk_id, attachments, message = return_message(personal_token, vk, event, counter, event.user_id,
                                                                     search_result, ids)

            elif request == 'В чёрный список':
                add_to_vk_blacklist(event.user_id, vk, vk_id)

            elif request == 'В избранное':
                add_to_vk_favorites(event.user_id, vk, vk_id, message, attachments)

            elif request == 'Мои избранные':
                favorites = select_all_favorites(event.user_id)
                count = 0
                while count < len(favorites):
                    return_favorites_list(favorites, vk, count, event.user_id)
                    count += 1

            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
