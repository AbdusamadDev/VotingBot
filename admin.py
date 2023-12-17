from main import disp, types


@disp.message_handler(commands=["test"])
async def testing(message: types.Message):
    await message.answer("hello")
