from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, executor, Dispatcher, types
from aiogram.dispatcher import FSMContext
import logging
import random

from buttons import teachers_list
from states import VotingState
from database import Database
from utils import (
    get_teachers_name,
    get_credentials,
    captcha_images,
    generate_list,
)


storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token="6473668158:AAGI-btt6VaDgOsaEiVLxQbVPVYQ0ErYfo8")
names_list = generate_list(names=get_teachers_name())
disp = Dispatcher(bot, storage=storage)
subscribtion_click = {}
database = Database()
start_page = 0
end_page = 8
ADMIN_ID = get_credentials().get("admin_id", None)


async def pagination(callback_query):
    await bot.delete_message(
        callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Ovoz berish uchun quyidagi o'qituvchilardan birini tanlang:\n\n"
        + "".join(names_list[start_page:end_page]),
        reply_markup=teachers_list(
            start_page=start_page,
            end_page=end_page,
            labels=list(get_teachers_name().keys()),
        ),
    )


@disp.message_handler(commands=["start"])
async def start(message: types.Message):
    if ADMIN_ID + 5 != message.from_user.id:
        if database.is_already_voted(message.from_user.id):
            await message.answer("Siz allaqachon ovoz berib bolgansiz!")
        else:
            global start_page, end_page
            start_page, end_page = 0, 8
            constructed_names = "".join(names_list[:end_page])
            await message.answer(
                f"Ovoz berish uchun quyidagi o'qituvchilardan birini tanlang:\n\n"
                + constructed_names,
                reply_markup=teachers_list(
                    start_page=start_page,
                    end_page=end_page,
                    labels=list(get_teachers_name().keys()),
                ),
            )
            database.add_user(
                telegram_id=message.from_user.id,
                first_name=message.from_user.first_name,
                username=message.from_user.username,
            )
    else:
        await message.answer("Wassup Admin, fuckin admin")


@disp.callback_query_handler(lambda query: query.data == "next")
async def next_handler(callback_query: types.CallbackQuery):
    global start_page, end_page
    end_page += 8
    start_page = end_page - 8
    await pagination(callback_query)


@disp.callback_query_handler(lambda query: query.data == "back")
async def back_handler(callback_query: types.CallbackQuery):
    global start_page, end_page
    end_page -= 8
    start_page = end_page - 8
    await pagination(callback_query)


@disp.callback_query_handler(lambda query: str(query.data).startswith("School"))
async def choice(callback_query: types.CallbackQuery, state: FSMContext):
    if database.is_already_voted(callback_query.from_user.id):
        await bot.send_message(
            "Siz allaqachon ovoz berib bolgansiz!", chat_id=callback_query.from_user.id
        )
    else:
        choice_data = callback_query.data.split(":")[-1]
        print("Mana osha ko't: ", callback_query.data)
        generated_captcha = random.choice(captcha_images)
        await VotingState.choice.set()
        await state.update_data(choice=choice_data, captcha=generated_captcha)
        await bot.send_photo(
            chat_id=callback_query.from_user.id, photo=open(generated_captcha[0], "rb")
        )
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f"Quyidagi rasmda nechi raqam berilgan?",
        )


@disp.message_handler(state=VotingState.choice)
async def process_choice(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == data.get("captcha")[1]:
        data = await state.get_data()
        choice_data = data.get("choice")
        print("Choice Data: ", choice_data)
        await bot.send_message(
            message.chat.id,
            f"Ovoz berganingiz uchun tashakkur!",
        )
        print(choice_data)
        database.voting(message.from_user.id, choice_data)
        await state.finish()
    else:
        await bot.send_message(
            message.chat.id, "Captcha noto'g'ri, qayta urinib ko'ring"
        )


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)
