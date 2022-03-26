from aiogram.dispatcher.filters.state import StatesGroup, State


class OrdersNearbyStates(StatesGroup):
    get_location = State()


