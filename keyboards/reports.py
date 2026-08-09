from aiogram.utils.keyboard import InlineKeyboardBuilder


def reports_menu():

    kb = InlineKeyboardBuilder()

    kb.button(

        text="📊 داشبورد",

        callback_data="report_dashboard",

    )

    kb.button(

        text="📅 گزارش امروز",

        callback_data="report_today",

    )

    kb.button(

        text="💰 گزارش مالی",

        callback_data="report_finance",

    )

    kb.button(

        text="📝 گزارش رزرو",

        callback_data="report_bookings",

    )

    kb.button(

        text="👥 گزارش پرسنل",

        callback_data="report_staff",

    )

    kb.button(

        text="📈 آمار",

        callback_data="report_statistics",

    )

    kb.button(

        text="🔙 بازگشت",

        callback_data="admin",

    )

    kb.adjust(

        2,

        2,

        2,

        1,

    )

    return kb.as_markup()