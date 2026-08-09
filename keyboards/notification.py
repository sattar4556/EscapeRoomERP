from aiogram.utils.keyboard import InlineKeyboardBuilder


def notification_menu():

    kb = InlineKeyboardBuilder()

    kb.button(

        text="📢 پیام همگانی",

        callback_data="notification_all",

    )

    kb.button(

        text="👥 پیام به پرسنل",

        callback_data="notification_staff",

    )

    kb.button(

        text="🎮 پیام به بازیکنان",

        callback_data="notification_players",

    )

    kb.button(

        text="⭐ پیام به VIP",

        callback_data="notification_vip",

    )

    kb.button(

        text="📋 تاریخچه ارسال",

        callback_data="notification_history",

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
