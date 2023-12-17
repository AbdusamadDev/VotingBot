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


async def check_subscription(user_id):
    try:
        # Get chat member info
        chat_member = await bot.get_chat_member(
            chat_id="https://t.me/LAYFXAK_KANAL", user_id=user_id
        )

        # Check if the user is a member of the channel
        print("Status: ", chat_member)
        if chat_member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False

    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        return False


@disp.message_handler(commands=["get"])
async def start(message: types.Message):
    user_id = message.from_user.id

    if await check_subscription(user_id):
        await message.reply("You are subscribed to the channel!")
    else:
        await message.reply(
            "To access this bot, you need to subscribe to the channel first."
        )


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)
