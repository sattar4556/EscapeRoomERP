from aiogram.utils.keyboard import InlineKeyboardBuilder


# ==========================================================
# GAMES KEYBOARD
# ==========================================================

def get_games_keyboard(games):
    kb = InlineKeyboardBuilder()

    for game in games:
        kb.button(
            text=f"🎮 {game.title}",
            callback_data=f"game_{game.id}"
        )

    kb.adjust(1)

    return kb.as_markup()


# ==========================================================
# SESSIONS KEYBOARD
# ==========================================================

def get_sessions_keyboard(sessions, game_id):
    kb = InlineKeyboardBuilder()

    for session in sessions:
        session_date = getattr(session, "date", None)
        start_time = getattr(session, "start_time", None)

        if session_date and start_time:
            text = f"📅 {session_date} | 🕐 {start_time}"
        elif start_time:
            text = f"🕐 {start_time}"
        elif session_date:
            text = f"📅 {session_date}"
        else:
            text = f"🎬 سانس #{session.id}"

        kb.button(
            text=text,
            callback_data=f"session_{session.id}"
        )

    kb.button(
        text="🔙 بازگشت به بازی‌ها",
        callback_data="back_to_games"
    )

    kb.adjust(1)

    return kb.as_markup()


# ==========================================================
# BOOKING CONFIRMATION KEYBOARD
# ==========================================================

def get_booking_confirm_keyboard(booking_id):
    kb = InlineKeyboardBuilder()

    kb.button(
        text="💳 پرداخت و قطعی کردن رزرو",
        callback_data=f"pay_{booking_id}"
    )

    kb.button(
        text="❌ لغو رزرو",
        callback_data=f"cancel_booking_{booking_id}"
    )

    kb.adjust(1)

    return kb.as_markup()