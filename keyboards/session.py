from aiogram.utils.keyboard import InlineKeyboardBuilder


def session_menu():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="➕ ساخت سانس",
        callback_data="session_add"
    )

    kb.button(
        text="📅 سانس‌های امروز",
        callback_data="session_today"
    )

    kb.button(
        text="📆 سانس‌های فردا",
        callback_data="session_tomorrow"
    )

    kb.button(
        text="🎟 همه سانس‌ها",
        callback_data="session_all"
    )

    kb.button(
        text="⬅️ هفته قبل",
        callback_data="session_prev_week"
    )

    kb.button(
        text="➡️ هفته بعد",
        callback_data="session_next_week"
    )

    kb.button(
        text="🔙 پنل مدیریت",
        callback_data="admin"
    )

    kb.adjust(
        2,
        2,
        2,
        1
    )

    return kb.as_markup()