from aiogram import Dispatcher

from loader import dp
from .admin import AdminOnly

from loader import dp


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminOnly)



