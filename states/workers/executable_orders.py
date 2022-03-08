from aiogram.dispatcher.filters.state import StatesGroup, State


class ExecutableOrdersStates(StatesGroup):
    get_order = State()


