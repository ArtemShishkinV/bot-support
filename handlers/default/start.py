from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api import db_postgres
from handlers.default import authorize_kodland


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await db_postgres.get_user_by_id(message.from_user.id)
    if user is not None:
        await message.answer(f'Привет, ты уже зарегистрирован!\n'
                             f'{user}')
    else:
        await authorize_kodland.start(message)
    await message.delete()
