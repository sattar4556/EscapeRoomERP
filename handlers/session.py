from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states.session import AddSession

from database.crud import (
    get_games,
    get_game_by_id,
    create_session,
)


router = Router()


# ==========================================================
# ADD SESSION
# ==========================================================

@router.callback_query(F.data == "add_session")
async def add_session(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.answer()

    games = await get_games()

    if not games:
        await callback.message.answer(
            "❌ اول باید حداقل یک بازی ثبت کنی."
        )
        return

    text = "🎮 لیست بازی‌ها\n\n"

    for game in games:
        text += f"{game.id} - {game.title}\n"

    await state.set_state(
        AddSession.game
    )

    await callback.message.answer(
        text + "\n\nشماره بازی را وارد کن:"
    )


# ==========================================================
# SELECT GAME
# ==========================================================

@router.message(AddSession.game)
async def session_game(
    message: Message,
    state: FSMContext
):
    if not message.text.isdigit():
        await message.answer(
            "❌ لطفاً شناسه بازی را به صورت عدد وارد کن."
        )
        return

    game_id = int(message.text)

    game = await get_game_by_id(
        game_id
    )

    if not game:
        await message.answer(
            "❌ بازی مورد نظر پیدا نشد."
        )
        return

    await state.update_data(
        game_id=game_id,
        game_duration=game.duration,
    )

    await state.set_state(
        AddSession.branch
    )

    await message.answer(
        "📍 شناسه شعبه:\n\n"
        "فعلاً 1 وارد کن."
    )


# ==========================================================
# BRANCH
# ==========================================================

@router.message(AddSession.branch)
async def session_branch(
    message: Message,
    state: FSMContext
):
    if not message.text.isdigit():
        await message.answer(
            "❌ شناسه شعبه باید عدد باشد."
        )
        return

    branch_id = int(
        message.text
    )

    await state.update_data(
        branch_id=branch_id
    )

    await state.set_state(
        AddSession.date
    )

    await message.answer(
        "📅 تاریخ سانس را وارد کن.\n\n"
        "مثال:\n"
        "2026-08-15"
    )


# ==========================================================
# DATE
# ==========================================================

@router.message(AddSession.date)
async def session_date(
    message: Message,
    state: FSMContext
):
    date_text = message.text.strip()

    try:
        datetime.strptime(
            date_text,
            "%Y-%m-%d"
        )

    except ValueError:
        await message.answer(
            "❌ فرمت تاریخ صحیح نیست.\n\n"
            "فرمت صحیح:\n"
            "2026-08-15"
        )
        return

    await state.update_data(
        date=date_text
    )

    await state.set_state(
        AddSession.time
    )

    await message.answer(
        "🕐 ساعت شروع سانس را وارد کن.\n\n"
        "مثال:\n"
        "19:00"
    )


# ==========================================================
# TIME
# ==========================================================

@router.message(AddSession.time)
async def session_time(
    message: Message,
    state: FSMContext
):
    time_text = message.text.strip()

    try:
        datetime.strptime(
            time_text,
            "%H:%M"
        )

    except ValueError:
        await message.answer(
            "❌ فرمت ساعت صحیح نیست.\n\n"
            "فرمت صحیح:\n"
            "19:00"
        )
        return

    await state.update_data(
        time=time_text
    )

    await state.set_state(
        AddSession.capacity
    )

    await message.answer(
        "👥 ظرفیت این سانس چند نفر است؟"
    )


# ==========================================================
# CAPACITY
# ==========================================================

@router.message(AddSession.capacity)
async def session_capacity(
    message: Message,
    state: FSMContext
):
    if not message.text.isdigit():
        await message.answer(
            "❌ ظرفیت باید عدد باشد."
        )
        return

    capacity = int(
        message.text
    )

    if capacity <= 0:
        await message.answer(
            "❌ ظرفیت باید بیشتر از صفر باشد."
        )
        return

    await state.update_data(
        capacity=capacity
    )

    await state.set_state(
        AddSession.price
    )

    await message.answer(
        "💰 قیمت این سانس را وارد کن.\n\n"
        "مثال:\n"
        "380000"
    )


# ==========================================================
# CREATE SESSION
# ==========================================================

@router.message(AddSession.price)
async def session_price(
    message: Message,
    state: FSMContext
):
    if not message.text.isdigit():
        await message.answer(
            "❌ قیمت باید به صورت عدد وارد شود."
        )
        return

    price = int(
        message.text
    )

    if price < 0:
        await message.answer(
            "❌ قیمت نمی‌تواند منفی باشد."
        )
        return

    data = await state.get_data()

    try:
        start_time = datetime.strptime(
            f"{data['date']} {data['time']}",
            "%Y-%m-%d %H:%M"
        )

    except ValueError:
        await message.answer(
            "❌ تاریخ یا ساعت نامعتبر است."
        )
        return

    duration = int(
        data.get(
            "game_duration",
            0
        )
    )

    if duration <= 0:
        await message.answer(
            "❌ مدت زمان بازی معتبر نیست."
        )
        return

    end_time = (
        start_time +
        timedelta(minutes=duration)
    )

    session = await create_session(
        game_id=data["game_id"],
        start_time=start_time,
        end_time=end_time,
        capacity=data["capacity"],
    )

    await state.clear()

    await message.answer(
        "✅ سانس با موفقیت ثبت شد.\n\n"
        f"🆔 شناسه سانس: {session.id}\n"
        f"🎮 بازی: {data.get('game_id')}\n"
        f"📅 تاریخ: {data['date']}\n"
        f"🕐 شروع: {data['time']}\n"
        f"🕐 پایان: {end_time.strftime('%H:%M')}\n"
        f"👥 ظرفیت: {data['capacity']} نفر\n"
        f"💰 قیمت: {price:,} تومان"
    )