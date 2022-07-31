from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from utils.db_api.db_postgres import get_user_by_id


class IsRegister(BoundFilter):
    async def check(self, message: Message) -> bool:
        is_register = await get_user_by_id(message.from_user.id) is not None
        if not is_register:
            await message.answer(f'Данную команду могут использовать только зарегистрированные пользователи!\n'
                                 f'Сначала напиши /start')
            await message.delete()
        return is_register
