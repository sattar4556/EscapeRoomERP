from aiogram import BaseMiddleware

from aiogram.types import TelegramObject

from typing import Callable
from typing import Awaitable
from typing import Dict
from typing import Any

import logging


logger = logging.getLogger(

    "EscapeRoomERP"

)


class LoggingMiddleware(BaseMiddleware):

    async def __call__(

        self,

        handler: Callable[

            [TelegramObject, Dict[str, Any]],

            Awaitable[Any],

        ],

        event: TelegramObject,

        data: Dict[str, Any],

    ):

        if hasattr(

            event,

            "from_user",

        ):

            logger.info(

                "%s (%s)",

                event.from_user.full_name,

                event.from_user.id,

            )

        return await handler(

            event,

            data,

        )