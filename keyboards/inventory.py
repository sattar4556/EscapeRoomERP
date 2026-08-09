from aiogram.utils.keyboard import InlineKeyboardBuilder


def inventory_menu():

    kb = InlineKeyboardBuilder()

    kb.button(

        text="➕ ثبت کالا",

        callback_data="inventory_add",

    )

    kb.button(

        text="📦 لیست کالاها",

        callback_data="inventory_list",

    )

    kb.button(

        text="📥 ورود کالا",

        callback_data="inventory_in",

    )

    kb.button(

        text="📤 خروج کالا",

        callback_data="inventory_out",

    )

    kb.button(

        text="⚠ موجودی کم",

        callback_data="inventory_low",

    )

    kb.button(

        text="📊 گزارش انبار",

        callback_data="inventory_report",

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