from dataclasses import dataclass
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
REFERRER_BONUS_PERCENT = 5
DAY_IN_MINUTES = 1440
DAY_IN_SECONDS = 86400
REFERRER_COINS = 20

SHORT_DISTANCE = 500
MIDDLE_DISTANCE = 1000
LONG_DISTANCE = 1500


@dataclass
class Roles:
    customer = "customer"
    worker = "worker"
    admin = "admin"


@dataclass
class InlineKeyboardAnswers:
    agree = "Согласен"
    do_not_agree = "Не согласен"
    start = "Начать"
    get_back = "Вернуться"


@dataclass
class MainMenuCommands:
    need_help = "Нужна помощь"
    change_data = "Изменить анкету"
    tasks_nearby = "Задания рядом"
    workers_nearby = "Исполнители рядом"
    my_orders = "Ваши задания"
    balance = "Баланс"


@dataclass
class OrderStatuses:
    waiting_for_payment = "Ожидает оплаты"
    waiting_for_start = "Ожидает начала"
    waiting_for_finish = "Ожидает пожтверждения о завершении"
    in_progress = "В процессе"
    completed = "Завершен"


@dataclass
class TransactionStatuses:
    ...


@dataclass
class PaymentMethods:
    one_time = "one_time"
    coins = "coins"
    with_bonus = "with_bonus"


@dataclass
class Distance:
    meters: int
    customer_price: int
    worker_price: int


class Distances:

    def __init__(self):
        self.short = Distance(SHORT_DISTANCE, 30, 0)
        self.middle = Distance(MIDDLE_DISTANCE, 50, 10)
        self.long = Distance(LONG_DISTANCE, 0, 20)

    def get_worker_price_by_distance(self, distance: int) -> int:
        return {
            SHORT_DISTANCE: self.short.worker_price,
            MIDDLE_DISTANCE: self.middle.worker_price,
            LONG_DISTANCE: self.middle.worker_price
        }.get(distance)

    def get_customer_price_by_distance(self, distance: int) -> int:
        return {
            SHORT_DISTANCE: self.short.customer_price,
            MIDDLE_DISTANCE: self.middle.customer_price,
            LONG_DISTANCE: self.middle.customer_price
        }.get(distance)


distances = Distances()


