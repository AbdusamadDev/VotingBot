from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def teachers_list(start_page, end_page, labels):
    part_1 = (start_page, start_page + 4)
    part_2 = (start_page + 4, end_page)
    print(labels)

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

    back_button = InlineKeyboardButton(text="<< Avvalgisi", callback_data="back")
    next_button = InlineKeyboardButton(text="Keyingisi >>", callback_data="next")
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            create_teachers_list(part_1),
            create_teachers_list(part_2),
            [back_button, next_button],
        ]
    )
    return buttons
