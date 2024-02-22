from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def keyboard_search():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('Покажи ещё', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('В избранное', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('В чёрный список', color=VkKeyboardColor.NEGATIVE)
    keyboard.get_empty_keyboard()

    return keyboard.get_keyboard()
