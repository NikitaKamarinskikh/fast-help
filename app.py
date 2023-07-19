import os

import asyncio
import django

from loader import bot, storage


async def on_startup(dp):
    from utils import on_startup_notify
    import filters
    filters.setup(dp)
    import middlewares

    await set_default_commands(dp)


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


def setup_django():
    os.environ.setdefault(
         'DJANGO_SETTINGS_MODULE',
         'admin.admin.settings',
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': 'true'})
    django.setup()


if __name__ == '__main__':
    setup_django()
    from utils.set_bot_commands import set_default_commands
    from aiogram import executor
    from handlers import dp
    import tasks

    loop = asyncio.get_event_loop()
    loop.create_task(tasks.tasks.setup())

    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )


