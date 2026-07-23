from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.crud import create_or_update_user

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user, created = await create_or_update_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    if created:
        text = f"""🎉 سلام {user.first_name}

حساب شما با موفقیت ساخته شد."""
    else:
        text = f"""👋 خوش برگشتی {user.first_name}"""

    await message.answer(text)