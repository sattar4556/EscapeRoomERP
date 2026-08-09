import re


def validate_phone(

    phone,

):

    return bool(

        re.fullmatch(

            r"09\d{9}",

            str(phone),

        )

    )


def validate_players(

    players,

):

    try:

        players = int(

            players

        )

        return players > 0

    except Exception:

        return False


def validate_amount(

    amount,

):

    try:

        amount = int(

            amount

        )

        return amount >= 0

    except Exception:

        return False