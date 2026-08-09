from database.crud import (
    create_booking,
    get_booking,
    update_booking,
    delete_booking,
    get_session,
    update_session,
)


# ==========================================================
# CREATE BOOKING
# ==========================================================

async def reserve(

    session_id: int,

    customer_name: str,

    customer_phone: str,

    players: int,

    total_price: int,

    paid_amount: int,

):

    session = await get_session(

        session_id

    )

    if session is None:

        return False, "session_not_found"

    free = (

        session.capacity

        -

        session.reserved_players

    )

    if players > free:

        return False, "capacity"

    booking = await create_booking(

        session_id=session_id,

        customer_name=customer_name,

        customer_phone=customer_phone,

        players=players,

        total_price=total_price,

        paid_amount=paid_amount,

        payment_status=(

            "paid"

            if paid_amount >= total_price

            else "partial"

        ),

        status="reserved",

    )

    await update_session(

        session.id,

        reserved_players=

            session.reserved_players

            +

            players,

    )

    return True, booking


# ==========================================================
# CANCEL BOOKING
# ==========================================================

async def cancel_booking(

    booking_id: int,

):

    booking = await get_booking(

        booking_id

    )

    if booking is None:

        return False

    session = await get_session(

        booking.session_id

    )

    await update_session(

        session.id,

        reserved_players=

            max(

                0,

                session.reserved_players

                -

                booking.players,

            ),

    )

    await update_booking(

        booking.id,

        status="cancelled",

    )

    return True


# ==========================================================
# DELETE BOOKING
# ==========================================================

async def remove_booking(

    booking_id: int,

):

    booking = await get_booking(

        booking_id

    )

    if booking is None:

        return False

    session = await get_session(

        booking.session_id

    )

    await update_session(

        session.id,

        reserved_players=

            max(

                0,

                session.reserved_players

                -

                booking.players,

            ),

    )

    await delete_booking(

        booking.id

    )

    return True


# ==========================================================
# CHECK IN
# ==========================================================

async def check_in(

    booking_id: int,

):

    booking = await get_booking(

        booking_id

    )

    if booking is None:

        return False

    await update_booking(

        booking.id,

        status="checked_in",

    )

    return True


# ==========================================================
# FINISH GAME
# ==========================================================

async def finish_game(

    booking_id: int,

):

    booking = await get_booking(

        booking_id

    )

    if booking is None:

        return False

    await update_booking(

        booking.id,

        status="finished",

    )

    return True


# ==========================================================
# COMPLETE PAYMENT
# ==========================================================

async def complete_payment(

    booking_id: int,

):

    booking = await get_booking(

        booking_id

    )

    if booking is None:

        return False

    await update_booking(

        booking.id,

        paid_amount=

            booking.total_price,

        payment_status="paid",

    )

    return True
