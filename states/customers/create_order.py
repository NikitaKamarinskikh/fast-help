from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateOrderStates(StatesGroup):
    get_category = State()
    get_possible_category = State()
    # get_subcategory = State()
    get_name = State()
    get_location = State()
    get_phone = State()
    cat_write = State()
    get_additional_contacts = State()
    get_order_description = State()
    get_communication_method = State()
    get_order_start_date = State()
    get_order_execution_time = State()
    get_distance = State()
    get_payment_method = State()
    get_payment = State()

