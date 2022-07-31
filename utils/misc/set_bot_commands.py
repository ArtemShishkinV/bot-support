from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("contacts", "Контакты школы"),
        types.BotCommand("help", "Помощь"),
    ])


async def set_authorized_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("menu", "Открыть меню с основными командами"),
        types.BotCommand("contacts", "Контакты школы"),
        types.BotCommand("help", "Помощь"),
    ])
