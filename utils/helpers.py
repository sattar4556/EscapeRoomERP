from datetime import datetime

import random

import string


# ==========================================================
# DATE TIME
# ==========================================================

def now():

    return datetime.now()


def now_string():

    return datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"

    )


# ==========================================================
# RANDOM CODE
# ==========================================================

def random_code(

    length=6,

):

    return "".join(

        random.choice(

            string.digits

        )

        for _ in range(

            length

        )

    )


# ==========================================================
# BOOKING CODE
# ==========================================================

def booking_code():

    return "BK-" + random_code(

        8

    )


# ==========================================================
# SESSION CODE
# ==========================================================

def session_code():

    return "SN-" + random_code(

        6

    )


# ==========================================================
# INVOICE CODE
# ==========================================================

def invoice_code():

    return "INV-" + random_code(

        10

    )


# ==========================================================
# MONEY
# ==========================================================

def money(

    amount,

):

    try:

        return f"{int(amount):,}"

    except Exception:

        return "0"


# ==========================================================
# PHONE
# ==========================================================

def normalize_phone(

    phone,

):

    phone = str(

        phone

    ).replace(

        " ",

        "",

    )

    if phone.startswith(

        "+98"

    ):

        phone = "0" + phone[3:]

    return phone


# ==========================================================
# BOOL
# ==========================================================

def yes_no(

    value,

):

    return "✅" if value else "❌"