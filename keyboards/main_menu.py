from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 بازی‌ها")],
        [KeyboardButton(text="📅 رزروهای من")],
        [KeyboardButton(text="🎁 تخفیف‌ها")],
        [KeyboardButton(text="📞 پشتیبانی")],
    ],
    resize_keyboard=True
)