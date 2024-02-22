from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def keyboard_main():
    keyboard = VkKeyboard()

    keyboard.add_button('Найди мне пару', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Мои избранные', color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()
