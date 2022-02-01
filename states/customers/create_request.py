from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateRequest(StatesGroup):
    get_category = State()
    # get_subcategory = State()
    get_name = State()
    get_location = State()
    get_additional_contacts = State()
    get_task = State()
    get_communication_method = State()
    get_task_start_date = State()
    get_task_execution_time = State()

