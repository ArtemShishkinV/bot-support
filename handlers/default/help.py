from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


async def send_message(source):
    text = ("Общие: ",
            "/start - Авторизоваться в боте",
            "/contacts - контакты школы для связи",
            "/help - Получить справку",
            "После авторизации доступ к меню по команде - /menu")
    func = source.message if type(source) is types.CallbackQuery else source
    await func.answer("\n".join(text))


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.delete()
    await send_message(message)


@dp.callback_query_handler(text='help')
async def bot_help_menu(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await send_message(call)
    # await call.answer()
