from aiogram import Router
from aiogram import F

from aiogram.types import CallbackQuery

from database.crud import (

    get_booking,

    pay_cash,

    pay_card,

)

router = Router()


@router.callback_query(
    F.data.startswith("cash_")
)
async def cash(callback: CallbackQuery):

    booking_id = int(
        callback.data.split("_")[1]
    )

    booking = await get_booking(
        booking_id
    )

    await pay_cash(

        booking.id,

        booking.remain_amount,

        callback.from_user.id,

    )

    await callback.answer(
        "پرداخت نقدی ثبت شد.",
        show_alert=True,
    )


@router.callback_query(
    F.data.startswith("card_")
)
async def card(callback: CallbackQuery):

    booking_id = int(
        callback.data.split("_")[1]
    )

    booking = await get_booking(
        booking_id
    )

    await pay_card(

        booking.id,

        booking.remain_amount,

        "CARD",

        callback.from_user.id,

    )

    await callback.answer(
        "پرداخت کارتخوان ثبت شد.",
        show_alert=True,
    )