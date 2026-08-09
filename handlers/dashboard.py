from aiogram import Router

from aiogram import F

from aiogram.types import CallbackQuery

from keyboards.dashboard import dashboard_menu


router = Router()


# ==========================================================
# DASHBOARD
# ==========================================================

@router.callback_query(

    F.data == "dashboard"

)

async def dashboard(

    callback: CallbackQuery,

):

    await callback.answer()

    text = """

📊 داشبورد مدیریتی

💰 درآمد امروز:

0

💸 هزینه امروز:

0

🎮 رزرو امروز:

0

👥 پرسنل حاضر:

0

"""

    await callback.message.edit_text(

        text,

        reply_markup=dashboard_menu(),

    )


# ==========================================================
# REFRESH
# ==========================================================

@router.callback_query(

    F.data == "dashboard_refresh"

)

async def dashboard_refresh(

    callback: CallbackQuery,

):

    await callback.answer(

        "بروزرسانی شد."

    )
