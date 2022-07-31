from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from utils.db_api.db_postgres import check_role_by_user_id


class IsUser(BoundFilter):
    async def check(self, message: Message) -> bool:
        is_user = not await check_role_by_user_id(message.from_user.id, "support")
        if not is_user:
            await message.answer(f'Данную команду могут использовать только обычные пользователи!\n'
                                 f'Для того чтобы вернуться в меню напиши - /menu')
            await message.delete()
        return is_user