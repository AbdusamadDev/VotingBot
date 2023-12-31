from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils import month_names


def teachers_list(start_page, end_page, labels):
    # part_1 = (start_page, start_page + 4)
    # part_2 = (start_page + 4, end_page)

    def create_teachers_list(limit):
        result = []
        print(limit)
        for i in range(*limit):
            try:
                result.append(
                    [
                        InlineKeyboardButton(
                            text=str(labels[i][0]).split("m")[0] + "M " + labels[i][1],
                            callback_data=f"School:{labels[i][0]}",
                        )
                    ]
                )
            except IndexError:
                break
        return result

    back_button = InlineKeyboardButton(text="⬅ Avvalgisi", callback_data="back")
    next_button = InlineKeyboardButton(text="Keyingisi ➡", callback_data="next")
    directions = []
    if start_page != 0 and end_page != 8:
        directions.append(back_button)
    if start_page != 48 and end_page != 56:
        directions.append(next_button)
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            *create_teachers_list(limit=(start_page, end_page)),
            directions,
        ]
    )
    return buttons


def users_list(start_page, end_page, labels):
    part_1 = (start_page, start_page + 4)
    part_2 = (start_page + 4, end_page)

    def create_users_list(limit):
        result = []
        for i in range(*limit):
            try:
                result.append(
                    InlineKeyboardButton(
                        text=str(labels[i]), callback_data=f"advertise_user:{labels[i]}"
                    )
                )
            except IndexError:
                break
        return result

    back_button = InlineKeyboardButton(text="<< Avvalgisi", callback_data="users_back")
    next_button = InlineKeyboardButton(text="Keyingisi >>", callback_data="users_next")
    directions = []
    if start_page != 0 and end_page != 8:
        directions.append(back_button)
    if start_page != 20 and end_page != 24:
        directions.append(next_button)
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            create_users_list(part_1),
            create_users_list(part_2),
            directions,
        ]
    )
    return buttons


def admin_options():
    view_teachers_button = InlineKeyboardButton(
        text="O'qituvchilarni ko'rish", callback_data="view_teachers"
    )
    channel_add_button = InlineKeyboardButton(
        text="Kanal qo'shish", callback_data="add_channel"
    )
    advertise_button = InlineKeyboardButton(
        text="Foydalanuvchilarga reklama yuborish", callback_data="advertise"
    )
    set_activity_time_button = InlineKeyboardButton(
        text="Ovoz berish muddatini belgilash", callback_data="set_activity"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [view_teachers_button],
            [channel_add_button],
            [advertise_button],
            [set_activity_time_button],
        ]
    )
    return markup


def start_months_buttons():
    buttons = [
        InlineKeyboardButton(text=name, callback_data=f"start_month:{name}")
        for name in month_names
    ]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[*buttons[0:5]], [*buttons[5:9]], [*buttons[9:12]]]
    )
    return markup


def end_months_buttons():
    buttons = [
        InlineKeyboardButton(text=name, callback_data=f"end_month:{name}")
        for name in month_names
    ]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[*buttons[0:5]], [*buttons[5:9]], [*buttons[9:12]]]
    )
    return markup


def get_channels_buttons(channel_names):
    buttons = [
        [InlineKeyboardButton(text=name.split("/")[-1], url=f"https://t.me/{name[1:]}")]
        for name in channel_names
    ]
    subscribed_button = InlineKeyboardButton(
        text="Obuna bo'ldim", callback_data="subscribed"
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[*buttons, [subscribed_button]])
    return markup
