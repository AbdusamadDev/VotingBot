from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, executor, Dispatcher, types
from aiogram.dispatcher import FSMContext
import logging

from utils import get_teachers_name, generate_list
from buttons import teachers_list
from states import VotingState

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token="6473668158:AAGI-btt6VaDgOsaEiVLxQbVPVYQ0ErYfo8")
disp = Dispatcher(bot, storage=storage)
start_page = 0
end_page = 8
names_list = generate_list(names=get_teachers_name())


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
        chat_id=callback_query.from_user.id, text=f"Your choice: {choice[-1]}"
    )
    await VotingState.choice.set()
    await state.update_data(choice=choice)


@disp.message_handler(commands=["mysubscriptions"])
async def my_subscriptions(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        subscribed_channels = data.get("subscribed_channels", [])

    if subscribed_channels:
        await message.answer(
            "Your subscribed channels:\n" + "\n".join(subscribed_channels)
        )
    else:
        await message.answer("You have not subscribed to any channels yet.")


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)
