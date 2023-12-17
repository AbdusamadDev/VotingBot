from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, executor, Dispatcher, types
from aiogram.dispatcher import FSMContext
import logging
import random

from utils import get_teachers_name, generate_list
from buttons import teachers_list, get_channels
from states import VotingState
from database import Database

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token="6473668158:AAGI-btt6VaDgOsaEiVLxQbVPVYQ0ErYfo8")
names_list = generate_list(names=get_teachers_name())
disp = Dispatcher(bot, storage=storage)
subscribtion_click = {}
database = Database()
start_page = 0
end_page = 8
captcha_images = [("image.jpg", "2005"), ("image2.jpg", "5566")]


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
    choice = callback_query.data.split(":")
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=f"Ovoz berish uchun quyidagi kanallarga a'zo bo'lishingiz kerak:",
        reply_markup=get_channels(),
    )
    await VotingState.choice.set()
    await state.update_data(choice=choice)

@disp.callback_query_handler(lambda query: str(query.data).startswith("subscribed"))
async def subscription_handler(callback_query: types.CallbackQuery):
    # await VotingState.captcha.set()
    # generated_captcha = random.choice(captcha_images)   
    # await state.update_data(captcha=generated_captcha[0])
    await bot.send_message(
        text="Captchadan uting: manu nichchi?",
        chat_id=callback_query.from_user.id,
    )


# @disp.callback_query_handler(lambda query: str(query.data).startswith("Channel"))
# async def channel_button_handler(callback_query: types.CallbackQuery):
#     channel_url = next(
#         (
#             channel[0]
#             for channel in CHANNELS
#             if callback_query.data.endswith(channel[1])
#         ),
#         None,
#     )
#     if channel_url:
#         print(f"Clicked URL: {channel_url}")

#     print("Button click@@@@!!!!")
#     # VotingState.channel_name.set()
#     # await state.update_data(channel_name=callback_query.data.split(":")[1])


@disp.message_handler(state=VotingState.captcha)
async def captcha_handler(message: types.Message, state: FSMContext):
    user_answer = message.text.strip()
    correct_answer = (await state.get_data()).get("captcha")[1]
    print(user_answer)
    print(correct_answer)
    if user_answer == correct_answer:
        await message.answer("Captcha is correct! You are subscribed.")
        database.voting(message.from_user.id)
    else:
        await message.answer("Captcha is incorrect. Please try again.")
    await state.finish()


# CHANNEL_USERNAME = "@LAYFXAK_KANAL"


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)
