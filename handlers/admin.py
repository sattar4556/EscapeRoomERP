from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.admin import admin_menu
from keyboards.session import session_menu

router = Router()


@router.callback_query(F.data == "admin")
async def admin_panel(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        """🛠 پنل مدیریت

به پنل مدیریت خوش اومدی.

از این قسمت میتونی:

🎮 مدیریت بازی‌ها
📅 مدیریت سانس‌ها
👥 مدیریت پرسنل
📊 گزارشات
⚙ تنظیمات

رو انجام بدی.""",
        reply_markup=admin_menu()
    )


@router.callback_query(F.data == "admin_games")
async def admin_games(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        "🎮 مدیریت بازی‌ها",
        reply_markup=admin_menu()
    )


@router.callback_query(F.data == "admin_sessions")
async def admin_sessions(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        "📅 مدیریت سانس‌ها",
        reply_markup=session_menu()
    )


@router.callback_query(F.data == "admin_staff")
async def admin_staff(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        "👥 مدیریت پرسنل",
        reply_markup=admin_menu()
    )


@router.callback_query(F.data == "admin_reports")
async def admin_reports(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        "📊 گزارشات",
        reply_markup=admin_menu()
    )


@router.callback_query(F.data == "admin_settings")
async def admin_settings(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        "⚙ تنظیمات",
        reply_markup=admin_menu()
    )
    