from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def teachers_list(start_page, end_page, labels):
    part_1 = (start_page, start_page + 4)
    part_2 = (start_page + 4, end_page)

    def create_teachers_list(limit):
        result = []
        for i in range(*limit):
            try:
                result.append(
                    InlineKeyboardButton(
                        text=str(labels[i]), callback_data=f"School:{labels[i]}"
                    )
                )
            except IndexError:
                break
        return result
    print(start_page, end_page)
    back_button = InlineKeyboardButton(text="<< Avvalgisi", callback_data="back")
    next_button = InlineKeyboardButton(text="Keyingisi >>", callback_data="next")
    directions = []
    if start_page != 0 and end_page != 8:
        directions.append(back_button)
    if start_page != 48 and end_page != 56:
        directions.append(next_button)
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            create_teachers_list(part_1),
            create_teachers_list(part_2),
            directions,
        ]
    )
    return buttons
