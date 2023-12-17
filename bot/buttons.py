from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def teachers_list(start_page, end_page, labels):
    # labels: [("", "")]
    part_1 = (start_page, start_page + 4)
    part_2 = (start_page + 4, end_page)

    def create_teachers_list(limit):
        return [
            InlineKeyboardButton(
                text=str(labels[i][0]), callback_data=f"School:{labels[i][0]}"
            )
            for i in range(*limit)
        ]

    back_button = InlineKeyboardButton(text="<< Avvalgisi", callback_data="back")
    next_button = InlineKeyboardButton(text="Keyingisi >>", callback_data="next")
    directions = []
    if end_page >= 0:
        directions.append(back_button)
    if start_page <= len(labels):
        directions.append(next_button)
    print(directions)
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            create_teachers_list(part_1),
            create_teachers_list(part_2),
            directions,
        ]
    )
    return buttons


def get_users(usernames, start_page, end_page):
    buttons = [
        InlineKeyboardButton(text=username[1], callback_data=f"user:{username[0]}")
        for username in usernames
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return (
        markup
        if len(usernames) <= 8
        else teachers_list(start_page, end_page, labels=usernames)
    )


# CHANNELS = [("https://t.me/LAYFXAK_KANAL", "Layfxak kanal official")]


# def get_channels():
#     buttons = [
#         InlineKeyboardButton(
#             text=channel[-1], url=channel[0], callback_data=f"Channel:{channel[1]}"
#         )
#         for channel in CHANNELS
#     ]
#     subscribed_button = InlineKeyboardButton(
#         text="Obuna bo'ldim", callback_data="subscribed"
#     )
#     channels_buttons = InlineKeyboardMarkup(
#         inline_keyboard=[buttons, [subscribed_button]]
#     )
#     return channels_buttons
