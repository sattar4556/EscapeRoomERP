from aiogram import Router

from aiogram import F

from aiogram.types import CallbackQuery

from keyboards.crm import crm_menu


router = Router()


# ==========================================================
# CRM PANEL
# ==========================================================

@router.callback_query(

    F.data == "crm"

)

async def crm_panel(

    callback: CallbackQuery,

):

    await callback.answer()

    await callback.message.edit_text(

        "👥 مدیریت مشتریان",

        reply_markup=crm_menu(),

    )


# ==========================================================
# ADD CUSTOMER
# ==========================================================

@router.callback_query(

    F.data == "crm_add"

)

async def crm_add(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# CUSTOMER LIST
# ==========================================================

@router.callback_query(

    F.data == "crm_list"

)

async def crm_list(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# DISCOUNT
# ==========================================================

@router.callback_query(

    F.data == "crm_discount"

)

async def crm_discount(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# VIP
# ==========================================================

@router.callback_query(

    F.data == "crm_vip"

)

async def crm_vip(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# BIRTHDAY
# ==========================================================

@router.callback_query(

    F.data == "crm_birthdays"

)

async def crm_birthdays(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# REPORT
# ==========================================================

@router.callback_query(

    F.data == "crm_report"

)

async def crm_report(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )