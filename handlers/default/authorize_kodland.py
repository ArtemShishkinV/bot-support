from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from states import UserState

from loader import dp

from keyboards.inline import kb_accept_email
from keyboards.inline.menu import menu_keyboard
from utils.db_api import db_postgres
from utils.misc.set_bot_commands import set_authorized_commands


async def start(message: types.Message):
    await UserState.login.set()
    await message.answer('Введи свой логин')
    await message.delete()


@dp.message_handler(state=UserState.login)
async def set_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    await UserState.next()
    await message.answer('Введи свой пароль')
    await message.delete()


@dp.message_handler(state=UserState.password)
async def set_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
        await message.delete()
        if await db_postgres.authorization_kodland(login=data['login'],
                                                   password=data['password']):
            data['kodland_user'] = await db_postgres.get_kodland_user_by_login(data['login'])
            await message.answer(f'Ваш email: {data["kodland_user"].email}\n'
                                 f'Выберите дальнейшее действие', reply_markup=kb_accept_email)
        else:
            await state.finish()
            await message.answer(f'Авторизация в системе Kodland не выполнена!\n'
                                 f'Если хотите попробовать еще раз - напишите /start')


@dp.callback_query_handler(Text(startswith='email_'), state=UserState.password)
async def accept_email_alert(call: CallbackQuery, state: FSMContext):
    response = call.data.split('_')[1]
    async with state.proxy() as data:
        if response == "accept":
            data['email'] = data['kodland_user'].email
            await state.finish()
            await db_postgres.create_user(call.from_user.id,
                                          call.from_user.full_name,
                                          data['kodland_user'])
            await call.answer()
            await finish_message(call)
        else:
            await call.message.answer('Введи новый email')
            await UserState.next()
        await call.message.edit_reply_markup()
        await call.answer()


@dp.message_handler(state=UserState.email)
async def accept_email_alert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
        await data['kodland_user'].update(email=data['email']).apply()
    await state.finish()
    await db_postgres.create_user(message.from_user.id,
                                  message.from_user.full_name,
                                  data['kodland_user'])
    await message.delete()
    await finish_message(message)


async def finish_message(source):
    await set_authorized_commands(dp)

    user = await db_postgres.get_user_by_id(source.from_user.id)
    text = f'Авторизация в системе kodland пройдена успешно!\n'
    f'Добро пожаловать!'

    func = source.message if type(source) is types.CallbackQuery else source
    await func.answer(text, reply_markup=await menu_keyboard(user))
