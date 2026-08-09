from aiogram import Router

from aiogram import F

from aiogram.types import CallbackQuery

from keyboards.backup import backup_menu


router = Router()


# ==========================================================
# BACKUP PANEL
# ==========================================================

@router.callback_query(

    F.data == "backup"

)

async def backup_panel(

    callback: CallbackQuery,

):

    await callback.answer()

    await callback.message.edit_text(

        "💾 مدیریت نسخه های پشتیبان",

        reply_markup=backup_menu(),

    )


# ==========================================================
# CREATE
# ==========================================================

@router.callback_query(

    F.data == "backup_create"

)

async def backup_create(

    callback: CallbackQuery,

):

    await callback.answer(

        "بعداً متصل می‌شود."

    )


# ==========================================================
# LIST
# ==========================================================

@router.callback_query(

    F.data == "backup_list"

)

async def backup_list(

    callback: CallbackQuery,

):

    await callback.answer(

        "بعداً متصل می‌شود."

    )


# ==========================================================
# RESTORE
# ==========================================================

@router.callback_query(

    F.data == "backup_restore"

)

async def backup_restore(

    callback: CallbackQuery,

):

    await callback.answer(

        "بعداً متصل می‌شود."

    )


# ==========================================================
# DELETE
# ==========================================================

@router.callback_query(

    F.data == "backup_delete"

)

async def backup_delete(

    callback: CallbackQuery,

):

    await callback.answer(

        "بعداً متصل می‌شود."

    )