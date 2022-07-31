from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from filters import IsRegister
from keyboards.inline.menu import menu_keyboard
from utils.db_api import db_postgres


@dp.message_handler(Command("menu"), IsRegister())
async def menu(message: types.Message):
    await message.delete()
    user = await db_postgres.get_user_by_id(message.from_user.id)
    await message.answer("Для продолжения выбери пункт из меню!", reply_markup=await menu_keyboard(user))
