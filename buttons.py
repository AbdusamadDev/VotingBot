from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils import get_teachers_name


def teachers_list(page_number):
    teachers_list = []
    for k in range(1, 3):
        print("K: ", k)
        print("Page number: ", page_number * 8)
        inner_list = []
        print("Rough Calculation: ", [1, 2][::-1][k - 1] * 4)
        for i in range((page_number * 8) - [1, 2][::-1][k - 1] * 4, page_number * 8):
            inner_list.append(
                InlineKeyboardButton(text=f"N{i}", callback_data=f"School:{i}")
            )
        teachers_list.append(inner_list)

    back_button = InlineKeyboardButton(text="<< Avvalgisi", callback_data="back")
    next_button = InlineKeyboardButton(text="Keyingisi >>", callback_data="next")
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[*teachers_list, [back_button, next_button]]
    )
    return buttons
