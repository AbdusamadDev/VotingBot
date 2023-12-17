from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def teachers_list(start_page, end_page, labels):
    part_1 = (start_page, start_page + 4)
    part_2 = (start_page + 4, end_page)
    teachers_list = lambda limit: [
        InlineKeyboardButton(text=labels[i], callback_data=f"School:{labels[i]}")
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


CHANNELS = [("https://t.me/LAYFXAK_KANAL", "Layfxak kanal official")]


def get_channels():
    buttons = [
        InlineKeyboardButton(
            text=channel[-1], url=channel[0], callback_data=f"Channel:{channel[0]}"
        )
        for channel in CHANNELS
    ]
    channels_buttons = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return channels_buttons
