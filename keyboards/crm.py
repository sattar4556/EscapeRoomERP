from aiogram.utils.keyboard import InlineKeyboardBuilder


def crm_menu():

    kb = InlineKeyboardBuilder()

    kb.button(

        text="👤 مشتری جدید",

        callback_data="crm_add",

    )

    kb.button(

        text="📋 لیست مشتریان",

        callback_data="crm_list",

    )

    kb.button(

        text="🎁 کد تخفیف",

        callback_data="crm_discount",

    )

    kb.button(

        text="⭐ مشتریان VIP",

        callback_data="crm_vip",

    )

    kb.button(

        text="🎂 تولد امروز",

        callback_data="crm_birthdays",

    )

    kb.button(

        text="📊 گزارش CRM",

        callback_data="crm_report",

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