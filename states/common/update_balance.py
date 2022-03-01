from aiogram.dispatcher.filters.state import StatesGroup, State


class UpdateBalanceStates(StatesGroup):
    get_payment = State()

