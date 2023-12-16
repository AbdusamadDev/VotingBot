from aiogram import Bot, executor, Dispatcher, types
import logging

from buttons import teachers_list

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6473668158:AAGI-btt6VaDgOsaEiVLxQbVPVYQ0ErYfo8")
disp = Dispatcher(bot)
page_number = 1


@disp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Hi, wassup", reply_markup=teachers_list(page_number))


@disp.callback_query_handler(lambda query: query.data == "next")
async def respond(callback_query: types.CallbackQuery):
    global page_number
    page_number += 1
    bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(
        callback_query.from_user.id,
        "You are an asshole!",
        reply_markup=teachers_list(page_number),
    )


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)
