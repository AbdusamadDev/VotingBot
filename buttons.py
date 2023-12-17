from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils import get_teachers_name


def teachers_list(page_number):
    teachers_list = [
        InlineKeyboardButton(text=f"N{i}", callback_data=f"School:{i}")
        for i in range((page_number * 4) - 4, page_number * 4)
    ]
    back_button = InlineKeyboardButton(text="<< Avvalgisi", callback_data="back")
    next_button = InlineKeyboardButton(text="Keyingisi >>", callback_data="next")
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[teachers_list, [back_button, next_button]]
    )
    return buttons
