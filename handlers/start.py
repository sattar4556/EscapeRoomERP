from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🎭 به ربات رسمی مجموعه اتاق فرار خوش آمدید.\n\n"
        "یکی از گزینه‌های زیر را انتخاب کنید.",
        reply_markup=main_menu
    )