from datetime import datetime


# ==========================================================
# MONEY
# ==========================================================

def format_money(

    amount,

    unit="تومان",

):

    try:

        amount = int(

            amount

        )

        return f"{amount:,} {unit}"

    except Exception:

        return f"0 {unit}"


# ==========================================================
# DATE
# ==========================================================

def format_date(

    date,

):

    if date is None:

        return "-"

    if isinstance(

        date,

        datetime,

    ):

        return date.strftime(

            "%Y-%m-%d"

        )

    return str(

        date

    )


# ==========================================================
# DATETIME
# ==========================================================

def format_datetime(

    date,

):

    if date is None:

        return "-"

    if isinstance(

        date,

        datetime,

    ):

        return date.strftime(

            "%Y-%m-%d %H:%M"

        )

    return str(

        date

    )


# ==========================================================
# PHONE
# ==========================================================

def format_phone(

    phone,

):

    phone = str(

        phone

    )

    if len(

        phone

    ) != 11:

        return phone

    return (

        phone[:4]

        + "-"

        + phone[4:7]

        + "-"

        + phone[7:]

    )


# ==========================================================
# STATUS
# ==========================================================

def format_status(

    status,

):

    mapping = {

        "reserved": "✅ رزرو",

        "checked_in": "🎮 شروع بازی",

        "finished": "🏁 پایان",

        "cancelled": "❌ لغو",

        "paid": "💰 تسویه",

        "partial": "💳 بیعانه",

        "pending": "⌛ پرداخت نشده",

        "open": "🟢 باز",

        "closed": "🔴 بسته",

    }

    return mapping.get(

        status,

        str(status),

    )