from aiogram.dispatcher.filters.state import State, StatesGroup


class VotingState(StatesGroup):
    telegram_id = State()
    first_name = State()
    username = State()
    captcha = State()
    choice = State()
