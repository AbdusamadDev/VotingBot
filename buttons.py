from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils import get_teachers_name


def teachers_list(start_page, end_page):
    teachers_list = lambda row: [
        InlineKeyboardButton(text=f"N{i}", callback_data=f"School:{i}")
        for i in range(start_page + 4, end_page)
    ]

    back_button = InlineKeyboardButton(text="<< Avvalgisi", callback_data="back")
    next_button = InlineKeyboardButton(text="Keyingisi >>", callback_data="next")
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[teachers_list, [back_button, next_button]]
    )
    print(start_page, end_page)
    print(teachers_list)
    return buttons
