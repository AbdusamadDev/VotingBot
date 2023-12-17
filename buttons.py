from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def teachers_list(start_page, end_page, labels):
    part_1 = (start_page, start_page + 4)
    part_2 = (start_page + 4, end_page)
    teachers_list = lambda limit: [
        InlineKeyboardButton(text=labels[i], callback_data=f"School:{i}")
        for i in range(*limit)
    ]
    back_button = InlineKeyboardButton(text="<< Avvalgisi", callback_data="back")
    next_button = InlineKeyboardButton(text="Keyingisi >>", callback_data="next")
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            teachers_list(part_1),
            teachers_list(part_2),
            [
                back_button if len(labels) >= 0 else [],
                next_button if len(labels) >= end_page else [],
            ],
        ]
    )
    return buttons
