from aiogram import Bot

from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramForbiddenError

from database.crud import (
    get_all_users,
)


# ==========================================================
# SEND MESSAGE
# ==========================================================

async def send_message(

    bot: Bot,

    telegram_id: int,

    text: str,

):

    try:

        await bot.send_message(

            chat_id=telegram_id,

            text=text,

        )

        return True

    except TelegramForbiddenError:

        return False

    except TelegramBadRequest:

        return False

    except Exception:

        return False


# ==========================================================
# BROADCAST
# ==========================================================

async def broadcast(

    bot: Bot,

    text: str,

):

    users = await get_all_users()

    success = 0

    failed = 0

    for user in users:

        result = await send_message(

            bot,

            user.telegram_id,

            text,

        )

        if result:

            success += 1

        else:

            failed += 1

    return {

        "success": success,

        "failed": failed,

        "total": len(users),

    }


# ==========================================================
# SEND TO LIST
# ==========================================================

async def send_to_users(

    bot: Bot,

    telegram_ids: list,

    text: str,

):

    success = 0

    failed = 0

    for telegram_id in telegram_ids:

        result = await send_message(

            bot,

            telegram_id,

            text,

        )

        if result:

            success += 1

        else:

            failed += 1

    return {

        "success": success,

        "failed": failed,

        "total": len(telegram_ids),

    }


# ==========================================================
# SEND TO STAFF
# ==========================================================

async def send_to_staff(

    bot: Bot,

    staffs,

    text: str,

):

    ids = []

    for staff in staffs:

        ids.append(

            staff.telegram_id

        )

    return await send_to_users(

        bot,

        ids,

        text,

    )


# ==========================================================
# SEND TO CUSTOMERS
# ==========================================================

async def send_to_customers(

    bot: Bot,

    customers,

    text: str,

):

    ids = []

    for customer in customers:

        ids.append(

            customer.telegram_id

        )

    return await send_to_users(

        bot,

        ids,

        text,

    )
