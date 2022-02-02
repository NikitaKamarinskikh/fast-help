from dataclasses import dataclass
from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов


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
    my_tasks = "Ваши задания"
    balance = "Баланс"
