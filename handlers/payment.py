from aiogram import Router, F

from aiogram.types import CallbackQuery

from database.crud import (
    get_booking,
    get_booking_remain_amount,
    pay_cash,
    pay_card,
)


router = Router()


# ==========================================================
# CASH PAYMENT
# ==========================================================

@router.callback_query(
    F.data.startswith("cash_")
)
async def cash(
    callback: CallbackQuery,
):

    booking_id = int(
        callback.data.split("_")[1]
    )

    booking = await get_booking(
        booking_id
    )

    if not booking:
        await callback.answer(
            "❌ رزرو پیدا نشد.",
            show_alert=True,
        )
        return

    remain_amount = (
        await get_booking_remain_amount(
            booking_id
        )
    )

    if remain_amount <= 0:
        await callback.answer(
            "✅ این رزرو قبلاً به طور کامل پرداخت شده است.",
            show_alert=True,
        )
        return

    payment = await pay_cash(
        booking_id=booking.id,
        amount=remain_amount,
        user_id=callback.from_user.id,
    )

    if not payment:
        await callback.answer(
            "❌ ثبت پرداخت انجام نشد.",
            show_alert=True,
        )
        return

    await callback.answer(
        f"✅ پرداخت نقدی به مبلغ "
        f"{remain_amount:,.0f} تومان ثبت شد.",
        show_alert=True,
    )


# ==========================================================
# CARD PAYMENT
# ==========================================================

@router.callback_query(
    F.data.startswith("card_")
)
async def card(
    callback: CallbackQuery,
):

    booking_id = int(
        callback.data.split("_")[1]
    )

    booking = await get_booking(
        booking_id
    )

    if not booking:
        await callback.answer(
            "❌ رزرو پیدا نشد.",
            show_alert=True,
        )
        return

    remain_amount = (
        await get_booking_remain_amount(
            booking_id
        )
    )

    if remain_amount <= 0:
        await callback.answer(
            "✅ این رزرو قبلاً به طور کامل پرداخت شده است.",
            show_alert=True,
        )
        return

    payment = await pay_card(
        booking_id=booking.id,
        amount=remain_amount,
        payment_type="CARD",
        user_id=callback.from_user.id,
    )

    if not payment:
        await callback.answer(
            "❌ ثبت پرداخت انجام نشد.",
            show_alert=True,
        )
        return

    await callback.answer(
        f"✅ پرداخت کارتخوان به مبلغ "
        f"{remain_amount:,.0f} تومان ثبت شد.",
        show_alert=True,
    )