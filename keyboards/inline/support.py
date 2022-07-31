import random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import dp
from utils.db_api import db_postgres
from utils.db_api.db_postgres import User

support_callback = CallbackData("ask_support", "messages", "user_id", "as_user")
cancel_support_callback = CallbackData("cancel_support", "user_id")


async def check_support_available(support_id):
    state = dp.current_state(chat=support_id, user=support_id)
    state_str = str(
        await state.get_state()
    )
    print(support_id)
    status_support = await db_postgres.get_user_by_id(support_id)
    if state_str != "in_support" and status_support.online:
        return support_id


async def get_support_manager():
    supports = await db_postgres.get_support_users()
    for support in supports:
        support_id = await check_support_available(support.chat_id)
        if support_id:
            return support_id
    else:
        return


async def support_keyboard(messages, user_id=None):
    if user_id:
        contact_id = int(user_id)
        as_user = "no"
        text = "Ответить пользователю"

    else:
        contact_id = await get_support_manager()
        as_user = "yes"
        if messages == "many" and contact_id is None:
            return False
        elif messages == "one" and contact_id is None:
            supports = await db_postgres.get_support_users()
            contact_id = random.choice(supports) if supports else 0
        if messages == "one":
            text = "Написать 1 сообщение в техподдержку"
        else:
            text = "Написать оператору"

    keyboard = InlineKeyboardMarkup()
    chat_id = contact_id.chat_id if type(contact_id) is User else contact_id
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=support_callback.new(
                messages=messages,
                user_id=chat_id,
                as_user=as_user
            )
        )
    )

    if messages == "many":
        keyboard.add(
            InlineKeyboardButton(
                text="Завершить сеанс",
                callback_data=cancel_support_callback.new(
                    user_id=contact_id
                )
            )
        )
    return keyboard


def cancel_support(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завершить сеанс",
                    callback_data=cancel_support_callback.new(
                        user_id=user_id
                    )
                )
            ]
        ]
    )
