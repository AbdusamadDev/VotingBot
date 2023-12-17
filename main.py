from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, executor, Dispatcher, types
from aiogram.dispatcher import FSMContext
import logging

from utils import get_teachers_name, generate_list
from buttons import teachers_list, get_channels
from states import VotingState

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token="6473668158:AAGI-btt6VaDgOsaEiVLxQbVPVYQ0ErYfo8")
names_list = generate_list(names=get_teachers_name())
disp = Dispatcher(bot, storage=storage)
subscribtion_click = {}
start_page = 0
end_page = 8


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
        chat_id=callback_query.from_user.id,
        text=f"Ovoz berish uchun quyidagi kanallarga a'zo bo'lishingiz kerak:",
        reply_markup=get_channels(),
    )
    await VotingState.choice.set()
    await state.update_data(choice=choice)


@disp.callback_query_handler(lambda query: query.data == "subscribed")
async def subscribtion_handler(callback_query: types.CallbackQuery, state: FSMContext):
    print(await state.get_data())
    await bot.send_message(
        text="Captchadan uting: manu nichchi 2255?", chat_id=callback_query.from_user.id
    )
    await VotingState.captcha.set()


@dp.inline_handler(lambda query: True)
async def inline_handler(query: types.InlineQuery):
    channels_buttons = get_channels()

    # Create an InlineQueryResultArticle with a link to the button
    result_id = "1"
    title = "Click me"
    input_message_content = types.InputTextMessageContent("You clicked the button!")
    inline_query_result = types.InlineQueryResultArticle(
        id=result_id,
        title=title,
        input_message_content=input_message_content,
        reply_markup=channels_buttons,
    )

    # Answer the inline query with the created result
    await bot.answer_inline_query(query.id, results=[inline_query_result])


@disp.callback_query_handler(lambda query: str(query.data).startswith("Channel"))
async def channel_button_handler(callback_query: types.CallbackQuery):
    # Extract the URL from the callback data
    channel_url = next(
        (
            channel[0]
            for channel in CHANNELS
            if callback_query.data.endswith(channel[1])
        ),
        None,
    )
    if channel_url:
        print(f"Clicked URL: {channel_url}")

    print("Button click@@@@!!!!")
    # VotingState.channel_name.set()
    # await state.update_data(channel_name=callback_query.data.split(":")[1])


# @disp.message_handler(state=VotingState.captcha)
# async def captcha_handler(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     print(f"Current state: {current_state}")
#     await state.finish()
#     await message.answer("Thank you for your response!")


CHANNEL_USERNAME = "@LAYFXAK_KANAL"


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)
