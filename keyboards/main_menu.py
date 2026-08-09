from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu():

    kb = InlineKeyboardBuilder()

    kb.button(text="🎟 رزرو سانس", callback_data="booking")
    kb.button(text="🎭 بازی‌ها", callback_data="games")

    kb.button(text="📅 رزروهای من", callback_data="my_bookings")
    kb.button(text="👤 پروفایل", callback_data="profile")

    kb.button(text="☎️ پشتیبانی", callback_data="support")
    kb.button(text="🛠 پنل مدیریت", callback_data="admin")

    kb.adjust(2, 2, 1, 1)

    return kb.as_markup()


def back_menu():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🔙 بازگشت",
        callback_data="home"
    )

    return kb.as_markup()