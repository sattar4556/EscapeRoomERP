from aiogram import Router

from aiogram import F

from aiogram.types import CallbackQuery

from keyboards.settings import settings_menu


router = Router()


# ==========================================================
# SETTINGS PANEL
# ==========================================================

@router.callback_query(

    F.data == "settings"

)

async def settings_panel(

    callback: CallbackQuery,

):

    await callback.answer()

    await callback.message.edit_text(

        "⚙ تنظیمات سیستم",

        reply_markup=settings_menu(),

    )


# ==========================================================
# ORGANIZATION
# ==========================================================

@router.callback_query(

    F.data == "settings_org"

)

async def settings_org(

    callback: CallbackQuery,

):

    await callback.answer(

        "بعداً تکمیل می‌شود."

    )


# ==========================================================
# ROLES
# ==========================================================

@router.callback_query(

    F.data == "settings_roles"

)

async def settings_roles(

    callback: CallbackQuery,

):

    await callback.answer(

        "بعداً تکمیل می‌شود."

    )


# ==========================================================
# NOTIFICATIONS
# ==========================================================

@router.callback_query(

    F.data == "settings_notifications"

)

async def settings_notifications(

    callback: CallbackQuery,

):

    await callback.answer(

        "بعداً تکمیل می‌شود."

    )


# ==========================================================
# BACKUP
# ==========================================================

@router.callback_query(

    F.data == "settings_backup"

)

async def settings_backup(

    callback: CallbackQuery,

):

    await callback.answer(

        "بعداً تکمیل می‌شود."

    )


# ==========================================================
# RESTORE
# ==========================================================

@router.callback_query(

    F.data == "settings_restore"

)

async def settings_restore(

    callback: CallbackQuery,

):

    await callback.answer(

        "بعداً تکمیل می‌شود."

    )


# ==========================================================
# SYSTEM
# ==========================================================

@router.callback_query(

    F.data == "settings_system"

)

async def settings_system(

    callback: CallbackQuery,

):

    await callback.answer(

        "بعداً تکمیل می‌شود."

    )
