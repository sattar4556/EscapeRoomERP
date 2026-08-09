from aiogram.utils.keyboard import InlineKeyboardBuilder


def backup_menu():

    kb = InlineKeyboardBuilder()

    kb.button(

        text="💾 تهیه نسخه پشتیبان",

        callback_data="backup_create",

    )

    kb.button(

        text="📂 لیست نسخه‌ها",

        callback_data="backup_list",

    )

    kb.button(

        text="♻ بازیابی",

        callback_data="backup_restore",

    )

    kb.button(

        text="🗑 حذف نسخه",

        callback_data="backup_delete",

    )

    kb.button(

        text="🔙 بازگشت",

        callback_data="admin",

    )

    kb.adjust(

        2,

        2,

        1,

    )

    return kb.as_markup()
