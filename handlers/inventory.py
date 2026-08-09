from aiogram import Router

from aiogram import F

from aiogram.types import CallbackQuery

from keyboards.inventory import inventory_menu


router = Router()


# ==========================================================
# INVENTORY PANEL
# ==========================================================

@router.callback_query(

    F.data == "inventory"

)

async def inventory_panel(

    callback: CallbackQuery,

):

    await callback.answer()

    await callback.message.edit_text(

        "📦 مدیریت انبار",

        reply_markup=inventory_menu(),

    )


# ==========================================================
# ADD ITEM
# ==========================================================

@router.callback_query(

    F.data == "inventory_add"

)

async def inventory_add(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# ITEM LIST
# ==========================================================

@router.callback_query(

    F.data == "inventory_list"

)

async def inventory_list(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# STOCK IN
# ==========================================================

@router.callback_query(

    F.data == "inventory_in"

)

async def inventory_in(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# STOCK OUT
# ==========================================================

@router.callback_query(

    F.data == "inventory_out"

)

async def inventory_out(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# LOW STOCK
# ==========================================================

@router.callback_query(

    F.data == "inventory_low"

)

async def inventory_low(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )


# ==========================================================
# REPORT
# ==========================================================

@router.callback_query(

    F.data == "inventory_report"

)

async def inventory_report(

    callback: CallbackQuery,

):

    await callback.answer(

        "در نسخه بعدی تکمیل می‌شود."

    )