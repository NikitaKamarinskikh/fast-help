from aiogram.dispatcher.filters.state import StatesGroup, State


class WorkerRegistrationStates(StatesGroup):
    get_category = State()
    # get_subcategory = State()
    get_name = State()
    get_location = State()
    get_phone = State()
    get_additional_contacts = State()



