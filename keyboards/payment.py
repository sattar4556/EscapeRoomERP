from aiogram.utils.keyboard import InlineKeyboardBuilder


def payment_menu(booking_id):

    kb = InlineKeyboardBuilder()

    kb.button(

        text="💵 نقدی",

        callback_data=f"cash_{booking_id}"

    )

    kb.button(

        text="💳 کارتخوان",

        callback_data=f"card_{booking_id}"

    )

    kb.button(

        text="🌐 آنلاین",

        callback_data=f"online_{booking_id}"

    )

    kb.button(

        text="🔙 بازگشت",

        callback_data="admin"

    )

    kb.adjust(2,1,1)

    return kb.as_markup()