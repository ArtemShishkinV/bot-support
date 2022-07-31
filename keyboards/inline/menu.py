from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api import db_postgres


async def menu_keyboard(user):
    kb_menu = InlineKeyboardMarkup(row_width=1)

    about_me_btn = InlineKeyboardButton('Обо мне', callback_data="about_me")
    help_btn = InlineKeyboardButton('Помощь', callback_data='help')
    contacts_btn = InlineKeyboardButton('Контакты школы', callback_data='contacts')

    role = await db_postgres.get_role_by_id(user.role_id)

    if role.title == 'support':
        call_support_btn = InlineKeyboardButton('Прекратить принимать запросы' if user.online else 'Выйти на связь',
                                                callback_data="change_status")
        send_support_btn = None
    else:
        send_support_btn = InlineKeyboardButton('Создать запрос в тех. поддержку', callback_data="send_support")
        call_support_btn = InlineKeyboardButton('Вызвать специалиста тех. поддержки', callback_data="call_support")

    kb_menu.add(about_me_btn, send_support_btn, call_support_btn, contacts_btn, help_btn) if send_support_btn \
        else kb_menu.add(about_me_btn, call_support_btn, contacts_btn, help_btn)

    return kb_menu
