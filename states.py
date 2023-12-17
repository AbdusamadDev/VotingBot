from aiogram.dispatcher.filters.state import State, StatesGroup


class VotingState(StatesGroup):
    choice = State()
    username = State()
    telegram_id = State()
    