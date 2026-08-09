from aiogram import BaseMiddleware

from aiogram.types import TelegramObject

from typing import Callable
from typing import Awaitable
from typing import Dict
from typing import Any

from database.crud import get_user


class AuthMiddleware(BaseMiddleware):

    async def __call__(

        self,

        handler: Callable[

            [TelegramObject, Dict[str, Any]],

            Awaitable[Any],

        ],

        event: TelegramObject,

        data: Dict[str, Any],

    ):

        user = None

        if hasattr(

            event,

            "from_user",

        ):

            user = await get_user(

                event.from_user.id,

            )

        data["current_user"] = user

        return await handler(

            event,

            data,

        )