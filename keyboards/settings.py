from aiogram.utils.keyboard import InlineKeyboardBuilder


def settings_menu():

    kb = InlineKeyboardBuilder()

    kb.button(

        text="🏢 اطلاعات مجموعه",

        callback_data="settings_org",

    )

    kb.button(

        text="👥 نقش‌ها",

        callback_data="settings_roles",

    )

    kb.button(

        text="🔔 اعلان‌ها",

        callback_data="settings_notifications",

    )

    kb.button(

        text="💾 تهیه نسخه پشتیبان",

        callback_data="settings_backup",

    )

    kb.button(

        text="♻ بازیابی نسخه پشتیبان",

        callback_data="settings_restore",

    )

    kb.button(

        text="⚙ تنظیمات سیستم",

        callback_data="settings_system",

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