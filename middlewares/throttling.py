import time

from aiogram import BaseMiddleware

from aiogram.types import TelegramObject

from typing import Callable
from typing import Awaitable
from typing import Dict
from typing import Any


class ThrottlingMiddleware(

    BaseMiddleware,

):

    def __init__(

        self,

        delay: float = 0.5,

    ):

        self.delay = delay

        self.cache = {}

    async def __call__(

        self,

        handler: Callable[

            [TelegramObject, Dict[str, Any]],

            Awaitable[Any],

        ],

        event: TelegramObject,

        data: Dict[str, Any],

    ):

        if not hasattr(

            event,

            "from_user",

        ):

            return await handler(

                event,

                data,

            )

        telegram_id = event.from_user.id

        now = time.time()

        last = self.cache.get(

            telegram_id,

            0,

        )

        if now - last < self.delay:

            return

        self.cache[

            telegram_id

        ] = now

        return await handler(

            event,

            data,

        )