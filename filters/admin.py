from aiogram.filters import BaseFilter

from aiogram.types import Message
from aiogram.types import CallbackQuery

from database.crud import get_user


class AdminFilter(BaseFilter):

    async def __call__(

        self,

        event: Message | CallbackQuery,

    ) -> bool:

        telegram_id = event.from_user.id

        user = await get_user(

            telegram_id

        )

        if user is None:

            return False

        return user.role == "admin"