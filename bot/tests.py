from aiogram import Bot, Dispatcher, types

API_TOKEN = "6473668158:AAGI-btt6VaDgOsaEiVLxQbVPVYQ0ErYfo8"

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def echo(message: types.Message):
    chat_member = await bot.get_chat_member(
        chat_id="@okDeveloper", user_id=message.from_user.id
    )
    print("Chat: ", chat_member)
    await message.answer("Asdasdasd")


if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
