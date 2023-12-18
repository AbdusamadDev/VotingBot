from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, executor, Dispatcher, types
from aiogram.utils.exceptions import BadRequest
from aiogram.dispatcher import FSMContext
from datetime import datetime
import calendar
import logging
import random

from database import Database
from states import (
    AdvertiseState,
    ChannelState,
    VotingState,
)
from buttons import (
    get_channels_buttons,
    start_months_buttons,
    end_months_buttons,
    teachers_list,
    admin_options,
    users_list,
)
from utils import (
    get_teachers_name,
    get_credentials,
    captcha_images,
    generate_list,
)

# 6746703582:AAFQFi1OEHizS6n3Gg7hI_Mt9IBFl43fTNc
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token="6473668158:AAGI-btt6VaDgOsaEiVLxQbVPVYQ0ErYfo8")
names_list = generate_list(names=get_teachers_name())
disp = Dispatcher(bot, storage=storage)
subscribtion_click = {}
database = Database()
users_names_list = generate_list(
    names={key: value for key, value in database.get_usernames()}
)
view_start_page = 0
view_end_page = 8
users_start_page = 0
users_end_page = 8
start_page = 0
end_page = 8
ADMIN_ID = get_credentials().get("admin_id", None)

# ====================================================================================
# ====================================================================================
# ===============================   USER ACTIONS   ===================================
# ====================================================================================
# ====================================================================================


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


@disp.callback_query_handler(lambda query: query.data.startswith("subscribed"))
async def subscribtion_check_handler(callback_query: types.CallbackQuery):
    print("WASSSUP")
    # unsubscribed_channels_two = []
    # channels = database.get_channels()
    # for channel_username in channels:
    #     try:
    #         chat_member = await bot.get_chat_member(
    #             chat_id=channel_username, user_id=callback_query.from_user.id
    #         )
    #         if chat_member.status != "member":
    #             unsubscribed_channels_two.append(channel_username)
    #     except BadRequest:
    #         await bot.send_message(
    #             chat_id=ADMIN_ID,
    #             text=f"Iltimos {channel_username} kanaliga botni admin qilib quying!",
    #         )
    # print(unsubscribed_channels_two)
    # if len(unsubscribed_channels_two) != 0:
    #     await bot.send_message(
    #         chat_id=callback_query.from_user.id,
    #         text="Please subscribe to these channels first:",
    #         reply_markup=get_channels_buttons(channels),
    #     )
    # else:
    #     await bot.send_message(
    #         chat_id=callback_query.from_user.id, text="You are freaking liar!!!!"
    #     )
    #     # generated_captcha = random.choice(captcha_images)
    #     # await bot.send_photo(
    #     #     chat_id=callback_query.from_user.id,
    #     #     photo=open(generated_captcha[0], "rb"),
    #     # )
    #     # await state.update_data(captcha=generated_captcha)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=f"Quyidagi rasmda nechi raqam berilgan?",
    )


@disp.callback_query_handler(lambda query: query.data == "asd")
async def example(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text="asdasdasasdas")


@disp.message_handler(commands=["start"])
async def start(message: types.Message):
    time_period = database.get_period()
    start_month_num = list(calendar.month_name).index(time_period[0].capitalize())
    end_month_num = list(calendar.month_name).index(time_period[1].capitalize())

    if ADMIN_ID + 5 != message.from_user.id:
        current_month = datetime.now().month
        if start_month_num <= current_month <= end_month_num or (
            start_month_num > end_month_num
            and (current_month >= start_month_num or current_month <= end_month_num)
        ):
            if database.is_already_voted(message.from_user.id):
                await message.answer("Siz allaqachon ovoz berib bolgansiz!")
            else:
                global start_page, end_page, users_start_page, users_end_page
                start_page, end_page = 0, 8
                users_start_page, users_end_page = 0, 8
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
            await message.answer("Hozir ovoz berish payti emas")
    else:
        await message.answer(
            "Assalomu alaykum admin!\nQuyidagilardan birini tanlang.",
            reply_markup=admin_options(),
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
    if database.is_already_voted(callback_query.from_user.id):
        await bot.send_message(
            "Siz allaqachon ovoz berib bolgansiz!", chat_id=callback_query.from_user.id
        )
    else:
        print("Is not voted yet, just preparing")
        choice_data = callback_query.data.split(":")[-1]
        await VotingState.choice.set()
        await state.update_data(choice=choice_data)
        unsubscribed_channels = []
        channels = database.get_channels()
        for channel_username in channels:
            print("Loop being executed")
            try:
                chat_member = await bot.get_chat_member(
                    chat_id=channel_username, user_id=callback_query.from_user.id
                )
                if chat_member.status != "member":
                    print("Unsubscribed channel found!")
                    unsubscribed_channels.append(channel_username)
            except BadRequest:
                await bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"Iltimos {channel_username} kanaliga botni admin qilib quying!",
                )
        if len(unsubscribed_channels) != 0:
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text="Please subscribe to these channels sdfsdfsdffirst:",
                reply_markup=get_channels_buttons(channels),
            )
        else:
            generated_captcha = random.choice(captcha_images)
            await bot.send_photo(
                chat_id=callback_query.from_user.id,
                photo=open(generated_captcha[0], "rb"),
            )
            await state.update_data(captcha=generated_captcha)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f"Quyidagi rasmda nechi raqam berilgan?",
            )


@disp.message_handler(state=VotingState.choice)
async def process_choice(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        if message.text == data.get("captcha")[1]:
            data = await state.get_data()
            choice_data = data.get("choice")
            await bot.send_message(
                message.chat.id,
                f"Ovoz berganingiz uchun tashakkur!",
            )
            database.voting(message.from_user.id, choice_data)
            await state.finish()
        else:
            await bot.send_message(
                message.chat.id, "Captcha noto'g'ri, qayta urinib ko'ring"
            )
    except:
        await message.answer("Botni /start orqali qayta ishga tushiring")


# ====================================================================================
# ====================================================================================
# ===============================   ADMIN ACTIONS   ==================================
# ====================================================================================
# ====================================================================================
async def users_pagination(callback_query):
    await bot.delete_message(
        callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.send_message(
        callback_query.from_user.id,
        text="Iltimos reklamani yuborish uchun bir necha yoki bitta "
        "foydalanuvchini tanlashingiz mumkin\n\n"
        + "".join(users_names_list[users_start_page:users_end_page]),
        reply_markup=users_list(
            start_page=users_start_page,
            end_page=users_end_page,
            labels=list(range(1, len(database.get_usernames()))),
        ),
    )


@disp.callback_query_handler(lambda query: query.data == "add_channel")
async def add_channel_handler(callback_query: types.CallbackQuery):
    await ChannelState.channel_name.set()
    await bot.send_message(
        callback_query.from_user.id,
        "Kanal nomini kiriting.\nEslatma, kanal nomini to'g'ri kiriting, "
        "foydalanuvchilar shu nom orqali kanalga qo'shilishadi",
    )


@disp.message_handler(state=ChannelState.channel_name)
async def channel_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(channel_name=message.text)
    data = await state.get_data()
    name = data.get("channel_name")
    await message.answer("Kanal qo'shildi!", reply_markup=admin_options())
    database.add_channel(name="@" + name)


@disp.callback_query_handler(lambda query: query.data == "advertise")
async def advertise_handler(callback_query: types.CallbackQuery):
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Iltimos reklamani yuborish uchun bir necha yoki bitta "
        "foydalanuvchini tanlashingiz mumkin\n\n"
        + "".join(users_names_list[users_start_page:users_end_page]),
        reply_markup=users_list(
            start_page=users_start_page,
            end_page=users_end_page,
            labels=list(range(users_start_page + 1, users_end_page + 1)),
        ),
    )


@disp.callback_query_handler(lambda query: query.data == "users_next")
async def users_next_handler(callback_query: types.CallbackQuery):
    global users_start_page, users_end_page
    users_end_page += 8
    users_start_page = users_end_page - 8
    await users_pagination(callback_query)


@disp.callback_query_handler(lambda query: query.data == "users_back")
async def users_back_handler(callback_query: types.CallbackQuery):
    global users_start_page, users_end_page
    users_end_page -= 8
    users_start_page = users_end_page - 8
    await users_pagination(callback_query)


@disp.callback_query_handler(lambda query: query.data.startswith("advertise_user"))
async def proceed_advertise_user_handler(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.send_message(
        text="Reklamangizni kiritishingiz mumkin!",
        chat_id=callback_query.from_user.id,
    )
    choice = callback_query.data.split(":")[-1]
    user = database.get_usernames()[int(choice) - 1][1]
    chat_id = database.get_user_id(user)
    await AdvertiseState.target_user.set()
    await state.update_data(target_user=int(chat_id))
    await AdvertiseState.advertise.set()


@disp.message_handler(
    content_types=types.ContentType.ANY, state=AdvertiseState.advertise
)
async def copy_advertise_and_send(message: types.Message, state: FSMContext):
    await message.answer(
        "Tashakkur, reklamangiz jo'natildi!", reply_markup=admin_options()
    )
    await state.update_data(advertise=message.text)
    data = await state.get_data()
    advertise = data.get("advertise")
    await bot.copy_message(
        chat_id=data.get("target_user"),
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        caption=advertise,
    )
    await state.finish()


@disp.callback_query_handler(lambda query: query.data == "view_teachers")
async def view_teachers(callback_query: types.CallbackQuery):
    await bot.send_message(
        text="".join(
            [
                f"{label} -- {votes} ta ovoz\n\n"
                for label, votes in database.get_teachers_by_order().items()
            ]
        ),
        chat_id=callback_query.from_user.id,
        reply_markup=admin_options(),
    )


@disp.callback_query_handler(lambda query: query.data == "set_activity")
async def set_activity_handler(callback_query: types.CallbackQuery):
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Ovoz berish muddatini kiriting, Boshlanish",
        reply_markup=start_months_buttons(),
    )


@disp.callback_query_handler(lambda query: query.data.startswith("start_month"))
async def set_start_month_handler(callback_query: types.CallbackQuery):
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Ovoz berish muddatini kiriting, Tugash",
        reply_markup=end_months_buttons(),
    )
    database.update_period(start_month=callback_query.data.split(":")[-1])


@disp.callback_query_handler(lambda query: query.data.startswith("end_month"))
async def set_end_month_handler(callback_query: types.CallbackQuery):
    await bot.send_message(
        text="Updated",
        chat_id=callback_query.from_user.id,
        reply_markup=admin_options(),
    )
    database.update_period(end_month=callback_query.data.split(":")[-1])


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)

# https://t.me/oKDeveloper
