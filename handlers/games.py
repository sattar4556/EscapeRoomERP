from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.crud import (
    get_games,
    get_game_by_id,
    get_available_sessions,
    create_booking,
    get_booking,
    add_payment,
    get_user,
)

from keyboards.games import (
    get_games_keyboard,
    get_sessions_keyboard,
    get_booking_confirm_keyboard,
)

from states.booking import BookingState


router = Router()


# ==========================================================
# SHOW GAMES
# ==========================================================

@router.message(F.text == "🎮 بازی‌ها")
async def show_games_menu(
    message: Message,
    state: FSMContext
):
    games = await get_games()

    if not games:
        await message.answer(
            "⚠️ در حال حاضر هیچ بازی فعالی ثبت نشده است."
        )
        return

    await state.set_state(
        BookingState.select_game
    )

    await message.answer(
        "🎮 لطفاً اتاق فرار مورد نظر خود را انتخاب کنید:",
        reply_markup=get_games_keyboard(games)
    )


# ==========================================================
# SELECT GAME
# ==========================================================

@router.callback_query(
    BookingState.select_game,
    F.data.startswith("game_")
)
async def select_game_callback(
    callback: CallbackQuery,
    state: FSMContext
):
    game_id = int(
        callback.data.split("_")[1]
    )

    game = await get_game_by_id(
        game_id
    )

    if not game:
        await callback.answer(
            "بازی مورد نظر یافت نشد.",
            show_alert=True
        )
        return

    # قیمت را فعلاً به صورت امن از مدل می‌خوانیم
    game_price = getattr(
        game,
        "price",
        getattr(game, "base_price", 0)
    )

    await state.update_data(
        game_id=game_id,
        game_title=game.title,
        game_price=game_price,
    )

    sessions = await get_available_sessions(
        game_id
    )

    if not sessions:
        await callback.message.edit_text(
            "⚠️ هیچ سانسی برای این بازی موجود نیست.",
            reply_markup=None
        )

        await state.clear()

        await callback.answer()

        return

    await state.set_state(
        BookingState.select_session
    )

    text = (
        f"🎬 <b>{game.title}</b>\n\n"
        f"🎭 ژانر: {game.genre}\n"
        f"⏱ مدت زمان: {game.duration} دقیقه\n"
        f"👥 تعداد بازیکنان: "
        f"{game.min_players} تا {game.max_players} نفر\n"
        f"💰 قیمت هر نفر: "
        f"{game_price:,.0f} تومان\n\n"
        f"👇 لطفاً سانس مورد نظر خود را انتخاب کنید:"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_sessions_keyboard(
            sessions,
            game_id
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# ==========================================================
# BACK TO GAMES
# ==========================================================

@router.callback_query(
    F.data == "back_to_games"
)
async def back_to_games_callback(
    callback: CallbackQuery,
    state: FSMContext
):
    games = await get_games()

    if not games:
        await callback.message.edit_text(
            "⚠️ در حال حاضر هیچ بازی فعالی ثبت نشده است."
        )

        await state.clear()

        await callback.answer()

        return

    await state.set_state(
        BookingState.select_game
    )

    await callback.message.edit_text(
        "🎮 لطفاً اتاق فرار مورد نظر خود را انتخاب کنید:",
        reply_markup=get_games_keyboard(games)
    )

    await callback.answer()


# ==========================================================
# SELECT SESSION
# ==========================================================

@router.callback_query(
    BookingState.select_session,
    F.data.startswith("session_")
)
async def select_session_callback(
    callback: CallbackQuery,
    state: FSMContext
):
    session_id = int(
        callback.data.split("_")[1]
    )

    await state.update_data(
        session_id=session_id
    )

    await state.set_state(
        BookingState.players
    )

    await callback.message.edit_text(
        "👥 لطفاً تعداد بازیکنان را به صورت یک عدد ارسال کنید.\n\n"
        "مثلاً: 4"
    )

    await callback.answer()


# ==========================================================
# ENTER PLAYERS
# ==========================================================

@router.message(
    BookingState.players,
    F.text
)
async def enter_players_count_handler(
    message: Message,
    state: FSMContext
):
    if not message.text.isdigit():
        await message.answer(
            "⚠️ لطفاً تعداد بازیکنان را به صورت عدد وارد کنید:"
        )
        return

    count = int(
        message.text
    )

    if count <= 0:
        await message.answer(
            "⚠️ تعداد بازیکنان باید بیشتر از صفر باشد."
        )
        return

    data = await state.get_data()

    price_per_person = data.get(
        "game_price",
        0
    )

    total_price = (
        count * price_per_person
    )

    user = await get_user(
        message.from_user.id
    )

    if not user:
        await message.answer(
            "لطفاً ابتدا با دستور /start ربات را راه‌اندازی کنید."
        )

        await state.clear()

        return

    booking = await create_booking(
        session_id=data.get("session_id"),
        user_id=user.id,
        players_count=count,
        total_price=total_price,
    )

    await state.update_data(
        booking_id=booking.id,
        players_count=count,
        total_price=total_price,
    )

    await state.set_state(
        BookingState.confirm
    )

    text = (
        "✅ <b>رزرو موقت شما ثبت شد!</b>\n\n"
        f"📌 شماره رزرو: #{booking.id}\n"
        f"🎬 بازی: {data.get('game_title')}\n"
        f"👥 تعداد بازیکنان: {count} نفر\n"
        f"💰 مبلغ کل: {total_price:,.0f} تومان\n\n"
        "برای قطعی شدن رزرو، لطفاً پرداخت را انجام دهید:"
    )

    await message.answer(
        text,
        reply_markup=get_booking_confirm_keyboard(
            booking.id
        ),
        parse_mode="HTML"
    )


# ==========================================================
# PAYMENT
# ==========================================================

@router.callback_query(
    BookingState.confirm,
    F.data.startswith("pay_")
)
async def payment_callback(
    callback: CallbackQuery,
    state: FSMContext
):
    booking_id = int(
        callback.data.split("_")[1]
    )

    booking = await get_booking(
        booking_id
    )

    if not booking:
        await callback.answer(
            "رزرو مورد نظر یافت نشد.",
            show_alert=True
        )
        return

    await add_payment(
        booking_id,
        booking.total_price,
        "online"
    )

    from database.database import SessionLocal
    from database.models import Booking

    async with SessionLocal() as db_session:
        booking_db = await db_session.get(
            Booking,
            booking_id
        )

        if booking_db:
            booking_db.status = "confirmed"

            await db_session.commit()

    await state.clear()

    await callback.message.edit_text(
        f"🎉 <b>پرداخت با موفقیت انجام شد!</b>\n\n"
        f"رزرو شماره #{booking_id} قطعی شد.\n\n"
        "منتظر حضور گرم شما هستیم! 🎭"
    )

    await callback.answer()