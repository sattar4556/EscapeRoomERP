from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.crud import create_or_update_user
from keyboards.main_menu import main_menu
from utils.messages import new_user, old_user

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
        await message.answer(
            new_user(user.first_name),
            reply_markup=main_menu()
        )
    else:
        await message.answer(
            old_user(user.first_name),
            reply_markup=main_menu()
        )