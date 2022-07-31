from aiogram import types

from filters import IsRegister, IsSupport
from loader import dp
from keyboards.inline.menu import menu_keyboard
from utils.db_api import db_postgres


@dp.callback_query_handler(IsRegister(), IsSupport(), text='change_status')
async def change_status(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user = await db_postgres.get_user_by_id(call.from_user.id)
    await user.update(online=not user.online).apply()
    text = 'Вы готовы принимать запросы от пользователей, ожидайте!' if user.online \
        else 'Для того чтобы начать принимать запросы нажмите "Выйти на связь"'
    await call.message.answer(text, reply_markup=await menu_keyboard(user))
