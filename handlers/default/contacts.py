from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from loader import dp


async def info(source):
    text = ("По всем организационным вопросам пишите нам: ",
            "✅ в Whatsapp по номеру +7 (995) 333-85-60 ",
            "✅ в Telegram @kodland_bot",
            "☎️ Или позвоните по номеру +7 (499) 490-72-77",
            "Хорошего дня! 😊")
    func = source.message if type(source) is types.CallbackQuery else source
    await func.answer("\n".join(text))


@dp.message_handler(Command("contacts"))
async def bot_contacts(message: types.Message):
    await message.delete()
    await info(message)


@dp.callback_query_handler(text="contacts")
async def bot_contacts_from_menu(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await info(call)
    await call.answer()
