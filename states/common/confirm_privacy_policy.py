from aiogram.dispatcher.filters.state import StatesGroup, State


class ConfirmPrivacyPolicy(StatesGroup):
    ask_to_confirm = State()
    get_answer = State()

