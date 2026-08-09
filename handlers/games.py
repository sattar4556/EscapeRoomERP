from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.crud import get_games, get_game_by_id, get_available_sessions, create_booking, get_booking, add_payment, get_user
from keyboards.games import get_games_keyboard, get_sessions_keyboard, get_booking_confirm_keyboard
from states.booking import BookingStates

router = Router()


@router.message(F.text == "🎮 بازی‌ها")
async def show_games_menu(message: Message, state: FSMContext):
    games = await get_games()
    if not games:
        await message.answer("⚠️ در حال حاضر هیچ بازی فعالی ثبت نشده است.")
        return

    await state.set_state(BookingStates.selecting_game)
    await message.answer("🎮 لطفاً اتاق فرار مورد نظر خود را انتخاب کنید:", reply_markup=get_games_keyboard(games))


@router.callback_query(BookingStates.selecting_game, F.data.startswith("game_"))
async def select_game_callback(callback: CallbackQuery, state: FSMContext):
    game_id = int(callback.data.split("_")[1])
    game = await get_game_by_id(game_id)
    if not game:
        await callback.answer("بازی مورد نظر یافت نشد.", show_alert=True)
        return

    await state.update_data(game_id=game_id, game_title=game.title, game_price=game.price)
    
    sessions = await get_available_sessions(game_id)
    if not sessions:
        await callback.message.edit_text("⚠️ هیچ سانسی برای این بازی موجود نیست.", reply_markup=None)
        await state.clear()
        return

    await state.set_state(BookingStates.selecting_session)
    text = f"""🎬 **{game.title}**
🎭 ژانر: {game.genre}
⏱ مدت زمان: {game.duration} دقیقه
👥 تعداد بازیکنان: {game.min_players} تا {game.max_players} نفر
💰 قیمت هر نفر: {game.price:,.0f} تومان

👇 لطفاً سانس مورد نظر خود را انتخاب کنید:"""

    await callback.message.edit_text(text, reply_markup=get_sessions_keyboard(sessions, game_id), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "back_to_games")
async def back_to_games_callback(callback: CallbackQuery, state: FSMContext):
    games = await get_games()
    await state.set_state(BookingStates.selecting_game)
    await callback.message.edit_text("🎮 لطفاً اتاق فرار مورد نظر خود را انتخاب کنید:", reply_markup=get_games_keyboard(games))
    await callback.answer()


@router.callback_query(BookingStates.selecting_session, F.data.startswith("session_"))
async def select_session_callback(callback: CallbackQuery, state: FSMContext):
    session_id = int(callback.data.split("_")[1])
    await state.update_data(session_id=session_id)

    await state.set_state(BookingStates.entering_players_count)
    await callback.message.edit_text("👥 لطفاً تعداد بازیکنان را به صورت یک عدد ارسال کنید (مثلاً 4):")
    await callback.answer()


@router.message(BookingStates.entering_players_count, F.text)
async def enter_players_count_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ لطفاً تعداد بازیکنان را به صورت عدد وارد کنید:")
        return

    count = int(message.text)
    data = await state.get_data()
    price_per_person = data.get("game_price", 0)
    total_price = count * price_per_person

    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("لطفاً ابتدا با دستور /start ربات را راه‌اندازی کنید.")
        await state.clear()
        return

    booking = await create_booking(
        session_id=data.get("session_id"),
        user_id=user.id,
        players_count=count,
        total_price=total_price
    )

    await state.clear()
    
    text = f"""✅ **رزرو موقت شما ثبت شد!**

📌 شماره رزرو: #{booking.id}
🎬 بازی: {data.get('game_title')}
👥 تعداد بازیکنان: {count} نفر
💰 مبلغ کل: {total_price:,.0f} تومان

برای قطعی شدن رزرو، لطفاً پرداخت را انجام دهید:"""

    await message.answer(text, reply_markup=get_booking_confirm_keyboard(booking.id), parse_mode="Markdown")


@router.callback_query(F.data.startswith("pay_"))
async def payment_callback(callback: CallbackQuery):
    booking_id = int(callback.data.split("_")[1])
    booking = await get_booking(booking_id)
    if not booking:
        await callback.answer("رزرو مورد نظر یافت نشد.", show_alert=True)
        return

    await add_payment(booking_id, booking.total_price, "online")
    
    from database.database import SessionLocal
    from database.models import Booking
    async with SessionLocal() as db_session:
        b = await db_session.get(Booking, booking_id)
        if b:
            b.status = "confirmed"
            await db_session.commit()

    await callback.message.edit_text(f"🎉 **پرداخت با موفقیت انجام شد!**\n\nرزرو شماره #{booking_id} قطعی شد. منتظر حضور گرم شما هستیم!", parse_mode="Markdown")
    await callback.answer()