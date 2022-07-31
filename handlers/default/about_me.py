from aiogram import types
from aiogram.dispatcher.filters.builtin import Text

from filters import IsRegister
from loader import dp
from utils.db_api import db_postgres
from keyboards.inline.menu import menu_keyboard


@dp.callback_query_handler(IsRegister(), Text('about_me'))
async def get_info_about_me_from_menu(call: types.CallbackQuery):
    await call.answer()

    user = await db_postgres.get_user_by_id(call.from_user.id)
    role = await db_postgres.get_role_by_id(user.role_id)
    kodland_user = await db_postgres.get_kodland_user_by_email(user.email)

    await call.message.answer(f'Telegram ID: {user.chat_id}\n'
                              f'Имя пользователя: {user.full_name}\n'
                              f'Email: {user.email}\n'
                              f'Логин Kodland: {kodland_user.login}\n'
                              f'Пароль Kodland: {kodland_user.password}\n'
                              f'Роль: {role.title}\n', reply_markup=await menu_keyboard(user))
    await call.message.delete()
