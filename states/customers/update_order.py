from aiogram.dispatcher.filters.state import StatesGroup, State


class UpdateOrderStates(StatesGroup):
    get_start_date = State()
    get_execution_time = State()


