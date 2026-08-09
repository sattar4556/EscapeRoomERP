from aiogram import Router

from aiogram import F

from aiogram.types import CallbackQuery

from keyboards.notification import notification_menu


router = Router()


# ==========================================================
# NOTIFICATION PANEL
# ==========================================================

@router.callback_query(

    F.data == "notifications"

)

async def notifications_panel(

    callback: CallbackQuery,

):

    await callback.answer()

    await callback.message.edit_text(

        "📢 مدیریت اعلان ها",

        reply_markup=notification_menu(),

    )


# ==========================================================
# SEND TO ALL
# ==========================================================

@router.callback_query(

    F.data == "notification_all"

)

async def notification_all(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# SEND TO STAFF
# ==========================================================

@router.callback_query(

    F.data == "notification_staff"

)

async def notification_staff(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# SEND TO PLAYERS
# ==========================================================

@router.callback_query(

    F.data == "notification_players"

)

async def notification_players(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# VIP
# ==========================================================

@router.callback_query(

    F.data == "notification_vip"

)

async def notification_vip(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# HISTORY
# ==========================================================

@router.callback_query(

    F.data == "notification_history"

)

async def notification_history(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )