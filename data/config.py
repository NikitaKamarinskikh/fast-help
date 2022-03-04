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




