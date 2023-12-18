from aiogram.dispatcher.filters.state import State, StatesGroup


class VotingState(StatesGroup):
    channel_name = State()
    telegram_id = State()
    first_name = State()
    username = State()
    captcha = State()
    choice = State()


class ChannelState(StatesGroup):
    channel_name = State()


class AdvertiseState(StatesGroup):
    target_user = State()
    advertise = State()


class TimePeriodState(StatesGroup):
    start_month = State()
    end_month = State()
    