from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.support import support_keyboard, support_callback
from keyboards.inline.menu import menu_keyboard
from utils.db_api import db_postgres
from loader import dp, bot
from filters import IsRegister, IsUser


@dp.callback_query_handler(IsRegister(), IsUser(), text='send_support')
async def ask_support_from_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup()
    text = "Хотите написать сообщение техподдержке? Нажмите на кнопку ниже!"
    keyboard = await support_keyboard(messages="one")
    await call.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages="one"))
async def send_to_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    await call.message.edit_reply_markup()

    user_id = int(callback_data.get("user_id"))
    if not user_id:
        user = await db_postgres.get_user_by_id(call.from_user.id)
        await call.message.answer("К сожалению, сейчас нет свободных операторов. Попробуйте позже.",
                                  reply_markup=await menu_keyboard(user))
        return

    await call.message.answer("Пришлите ваше сообщение, которым вы хотите поделиться")
    await state.set_state("wait_for_support_message")
    await state.update_data(second_id=user_id)


@dp.message_handler(state="wait_for_support_message", content_types=types.ContentTypes.ANY)
async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    await bot.send_message(second_id,
                           f"Вам письмо! Вы можете ответить нажав на кнопку ниже")
    keyboard = await support_keyboard(messages="one", user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)
    user = await db_postgres.get_user_by_id(message.from_user.id)
    await message.answer("Вы отправили это сообщение!", reply_markup=await menu_keyboard(user))
    await state.reset_state()
