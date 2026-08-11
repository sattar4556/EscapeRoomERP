from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states.booking import BookingState

from database.crud import (
    get_session,
    create_booking,
    get_user,
)

from keyboards.main_menu import back_menu


router = Router()


# ==========================================================
# START RESERVATION
# ==========================================================

@router.callback_query(
    F.data.startswith("reserve_")
)
async def reserve_start(
    callback: CallbackQuery,
    state: FSMContext,
):
    await callback.answer()

    session_id = int(
        callback.data.split("_")[1]
    )

    session = await get_session(
        session_id
    )

    if not session:
        await callback.message.edit_text(
            "❌ این سانس پیدا نشد."
        )
        return

    if not session.is_active:
        await callback.message.edit_text(
            "❌ این سانس غیرفعال شده است."
        )
        return

    await state.update_data(
        session_id=session_id
    )

    await state.set_state(
        BookingState.customer_name
    )

    await callback.message.edit_text(
        "🎟 <b>رزرو سانس</b>\n\n"
        "اسم رزرو کننده را ارسال کن.\n\n"
        "مثال:\n"
        "ستار آقادادی",
        parse_mode="HTML",
    )


# ==========================================================
# CUSTOMER NAME
# ==========================================================

@router.message(
    BookingState.customer_name
)
async def booking_name(
    message: Message,
    state: FSMContext,
):
    name = (
        message.text or ""
    ).strip()

    if not name:
        await message.answer(
            "❌ نام نمی‌تواند خالی باشد."
        )
        return

    await state.update_data(
        customer_name=name
    )

    await state.set_state(
        BookingState.customer_phone
    )

    await message.answer(
        "📱 شماره موبایل را ارسال کن.\n\n"
        "مثال:\n"
        "09123456789"
    )


# ==========================================================
# CUSTOMER PHONE
# ==========================================================

@router.message(
    BookingState.customer_phone
)
async def booking_phone(
    message: Message,
    state: FSMContext,
):
    phone = (
        message.text or ""
    ).strip()

    if not phone.isdigit():
        await message.answer(
            "❌ شماره موبایل باید فقط شامل عدد باشد."
        )
        return

    if len(phone) != 11:
        await message.answer(
            "❌ شماره موبایل باید ۱۱ رقم باشد."
        )
        return

    await state.update_data(
        customer_phone=phone
    )

    await state.set_state(
        BookingState.players
    )

    await message.answer(
        "👥 چند نفر هستید؟\n\n"
        "فقط عدد ارسال کن.\n\n"
        "مثال:\n"
        "5"
    )


# ==========================================================
# PLAYERS
# ==========================================================

@router.message(
    BookingState.players
)
async def booking_players(
    message: Message,
    state: FSMContext,
):
    if not message.text.isdigit():
        await message.answer(
            "❌ فقط عدد وارد کن."
        )
        return

    players = int(
        message.text
    )

    if players <= 0:
        await message.answer(
            "❌ تعداد نفرات باید بیشتر از صفر باشد."
        )
        return

    data = await state.get_data()

    session = await get_session(
        data["session_id"]
    )

    if not session:
        await message.answer(
            "❌ سانس مورد نظر پیدا نشد."
        )

        await state.clear()

        return

    if not session.is_active:
        await message.answer(
            "❌ این سانس دیگر فعال نیست."
        )

        await state.clear()

        return

    # ======================================================
    # CHECK CAPACITY
    # ======================================================

    if players > session.capacity:
        await message.answer(
            f"❌ ظرفیت این سانس فقط "
            f"{session.capacity} نفر است."
        )
        return

    # ======================================================
    # GET GAME
    # ======================================================

    game = session.game

    if not game:
        await message.answer(
            "❌ بازی مربوط به این سانس پیدا نشد."
        )

        await state.clear()

        return

    # ======================================================
    # CHECK GAME PLAYER LIMIT
    # ======================================================

    if players < game.min_players:
        await message.answer(
            f"❌ حداقل تعداد بازیکن برای این بازی "
            f"{game.min_players} نفر است."
        )
        return

    if players > game.max_players:
        await message.answer(
            f"❌ حداکثر تعداد بازیکن برای این بازی "
            f"{game.max_players} نفر است."
        )
        return

    # ======================================================
    # PRICE
    # ======================================================

    price_per_person = getattr(
        game,
        "base_price",
        0,
    )

    total_price = (
        players * price_per_person
    )

    # ======================================================
    # GET USER
    # ======================================================

    user = await get_user(
        message.from_user.id
    )

    if not user:
        await message.answer(
            "❌ اطلاعات کاربری شما پیدا نشد.\n\n"
            "لطفاً ابتدا /start را اجرا کنید."
        )

        await state.clear()

        return

    # ======================================================
    # CREATE BOOKING
    # ======================================================

    booking = await create_booking(
        session_id=session.id,
        user_id=user.id,
        players_count=players,
        total_price=total_price,
    )

    await state.clear()

    # ======================================================
    # SESSION DATE / TIME
    # ======================================================

    start_time = session.start_time

    date_text = start_time.strftime(
        "%Y-%m-%d"
    )

    time_text = start_time.strftime(
        "%H:%M"
    )

    # ======================================================
    # CONFIRMATION
    # ======================================================

    await message.answer(
        "🎉 <b>رزرو شما با موفقیت ثبت شد!</b>\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"🎭 <b>بازی:</b> {game.title}\n"
        f"📅 <b>تاریخ:</b> {date_text}\n"
        f"⏰ <b>ساعت:</b> {time_text}\n"
        f"👥 <b>تعداد نفرات:</b> {players}\n"
        f"💰 <b>مبلغ:</b> {total_price:,.0f} تومان\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"🧾 <b>شماره رزرو:</b> #{booking.id}\n\n"
        "رزرو شما در انتظار پرداخت است.",
        reply_markup=back_menu(),
        parse_mode="HTML",
    )