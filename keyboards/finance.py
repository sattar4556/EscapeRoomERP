from aiogram.utils.keyboard import InlineKeyboardBuilder


def finance_menu():

    kb = InlineKeyboardBuilder()

    kb.button(

        text="💰 ثبت درآمد",

        callback_data="finance_income",

    )

    kb.button(

        text="💸 ثبت هزینه",

        callback_data="finance_expense",

    )

    kb.button(

        text="👤 پرداخت حقوق",

        callback_data="finance_salary",

    )

    kb.button(

        text="📦 صندوق",

        callback_data="finance_cash",

    )

    kb.button(

        text="🏦 بانک",

        callback_data="finance_bank",

    )

    kb.button(

        text="📊 گزارش مالی",

        callback_data="finance_report",

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