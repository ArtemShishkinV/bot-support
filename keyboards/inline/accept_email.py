from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

accept_email_btn = InlineKeyboardButton('Подтвердить', callback_data='email_accept')
change_email_btn = InlineKeyboardButton('Сменить почту', callback_data='email_change')

kb_accept_email = InlineKeyboardMarkup().add(accept_email_btn, change_email_btn)
