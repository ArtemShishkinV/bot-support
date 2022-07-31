from aiogram import executor

from loader import dp

# Без этих импортов команды работать не будут
import middlewares
import filters
import handlers

from utils.db_api.db_postgres import create_db
from utils.misc.logging import logging
from utils.misc.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    await create_db()
    logging.info('Бот успешно запущен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
