from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def teachers_list(page_number):
    teachers_list = []
    for k in range(1, 3):
        print("K: ", k)
        print("Page number: ", page_number * 8)
        inner_list = []
        print("Rough Calculation: ", k * 4)
        print(f"From {(page_number * 8) - k * 4} To {page_number * 4 * k}")
        for i in range((page_number * 8) - k * 4, page_number * 4 * k):
            inner_list.append(
                InlineKeyboardButton(text=f"N{i}", callback_data=f"School:{i}")
            )
        teachers_list.append(inner_list)

    back_button = InlineKeyboardButton(text="<< Avvalgisi", callback_data="back")
    next_button = InlineKeyboardButton(text="Keyingisi >>", callback_data="next")
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[*teachers_list, [back_button, next_button]]
    )
    print(teachers_list)
    print("\n\n")
    return buttons
