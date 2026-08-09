from aiogram.utils.keyboard import InlineKeyboardBuilder


def dashboard_menu():

    kb = InlineKeyboardBuilder()

    kb.button(

        text="📊 بروزرسانی",

        callback_data="dashboard_refresh",

    )

    kb.button(

        text="📈 گزارشات",

        callback_data="admin_reports",

    )

    kb.button(

        text="💰 امور مالی",

        callback_data="finance",

    )

    kb.button(

        text="📅 سانس‌ها",

        callback_data="admin_sessions",

    )

    kb.button(

        text="👥 پرسنل",

        callback_data="admin_staff",

    )

    kb.button(

        text="🔙 بازگشت",

        callback_data="admin",

    )

    kb.adjust(

        2,

        2,

        1,

        1,

    )

    return kb.as_markup()
