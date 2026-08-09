from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.crud import (
    get_games,
    get_game,
    create_session,
    get_sessions,
)

from states.session import AddSessionState

router = Router()


# ==========================================================
# ADD SESSION
# ==========================================================

@router.callback_query(F.data == "session_add")
async def session_add(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    games = await get_games()

    if not games:

        await callback.message.edit_text(
            "❌ هیچ بازی ثبت نشده.\n\nابتدا یک بازی ایجاد کن."
        )

        return

    text = "🎮 بازی مورد نظر را انتخاب کن.\n\n"

    for game in games:

        text += f"{game.id} - {game.title}\n"

    await state.set_state(AddSessionState.game)

    await callback.message.edit_text(text)


@router.message(AddSessionState.game)
async def session_game(message: Message, state: FSMContext):

    game = await get_game(int(message.text))

    if not game:

        await message.answer("❌ شناسه بازی معتبر نیست.")

        return

    await state.update_data(
        game_id=game.id
    )

    await state.set_state(AddSessionState.date)

    await message.answer(

        """📅 تاریخ سانس را وارد کن.

مثال:

1405/05/12"""

    )


@router.message(AddSessionState.date)
async def session_date(message: Message, state: FSMContext):

    await state.update_data(
        date=message.text
    )

    await state.set_state(AddSessionState.time)

    await message.answer(

        """🕒 ساعت سانس را وارد کن.

مثال:

21:00"""

    )


@router.message(AddSessionState.time)
async def session_time(message: Message, state: FSMContext):

    await state.update_data(
        time=message.text
    )

    await state.set_state(AddSessionState.capacity)

    await message.answer(

        """👥 ظرفیت سانس؟

مثال:

8"""

    )


@router.message(AddSessionState.capacity)
async def session_capacity(message: Message, state: FSMContext):

    await state.update_data(
        capacity=int(message.text)
    )

    await state.set_state(AddSessionState.price)

    await message.answer(

        """💰 قیمت این سانس؟

مثال:

380000"""

    )


@router.message(AddSessionState.price)
async def session_price(message: Message, state: FSMContext):

    data = await state.get_data()

    await create_session(

        organization_id=1,

        branch_id=1,

        game_id=data["game_id"],

        session_date=data["date"],

        session_time=data["time"],

        capacity=data["capacity"],

        final_price=int(message.text),

    )

    await state.clear()

    await message.answer(

        """✅ سانس با موفقیت ساخته شد."""

    )


# ==========================================================
# SESSION LIST
# ==========================================================

@router.callback_query(F.data == "session_list")
async def session_list(callback: CallbackQuery):

    await callback.answer()

    sessions = await get_sessions()

    if not sessions:

        await callback.message.edit_text(

            "❌ هیچ سانسی ثبت نشده."

        )

        return

    text = "📅 لیست سانس‌ها\n\n"

    for session in sessions:

        text += (

            f"🆔 {session.id}\n"

            f"🎮 بازی: {session.game_id}\n"

            f"📅 {session.session_date}\n"

            f"🕒 {session.session_time}\n"

            f"👥 {session.reserved_players}/{session.capacity}\n"

            f"💰 {session.final_price:,}\n"

            f"📌 {session.status}\n\n"

        )

    await callback.message.edit_text(text)
    from states.session import (
    EditSessionState,
    DeleteSessionState,
    OpenSessionState,
    CloseSessionState,
    CancelSessionState,
)

from database.crud import (
    get_session,
    update_session,
    delete_session,
)


# ==========================================================
# DELETE SESSION
# ==========================================================

@router.callback_query(F.data == "session_delete")
async def session_delete(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(DeleteSessionState.session)

    await callback.message.edit_text(
        "🗑 شناسه سانس را ارسال کن."
    )


@router.message(DeleteSessionState.session)
async def session_delete_finish(message: Message, state: FSMContext):

    session = await get_session(int(message.text))

    if not session:

        await message.answer("❌ سانس پیدا نشد.")

        return

    await delete_session(session.id)

    await state.clear()

    await message.answer("✅ سانس حذف شد.")


# ==========================================================
# OPEN SESSION
# ==========================================================

@router.callback_query(F.data == "session_open")
async def session_open(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(OpenSessionState.session)

    await callback.message.edit_text(
        "🔓 شناسه سانس را ارسال کن."
    )


@router.message(OpenSessionState.session)
async def session_open_finish(message: Message, state: FSMContext):

    session = await get_session(int(message.text))

    if not session:

        await message.answer("❌ سانس پیدا نشد.")

        return

    await update_session(
        session.id,
        status="open"
    )

    await state.clear()

    await message.answer("✅ سانس باز شد.")


# ==========================================================
# CLOSE SESSION
# ==========================================================

@router.callback_query(F.data == "session_close")
async def session_close(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(CloseSessionState.session)

    await callback.message.edit_text(
        "🔒 شناسه سانس را ارسال کن."
    )


@router.message(CloseSessionState.session)
async def session_close_finish(message: Message, state: FSMContext):

    session = await get_session(int(message.text))

    if not session:

        await message.answer("❌ سانس پیدا نشد.")

        return

    await update_session(
        session.id,
        status="closed"
    )

    await state.clear()

    await message.answer("🔒 سانس بسته شد.")


# ==========================================================
# CANCEL SESSION
# ==========================================================

@router.callback_query(F.data == "session_cancel")
async def session_cancel(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(CancelSessionState.session)

    await callback.message.edit_text(
        "❌ شناسه سانس را ارسال کن."
    )


@router.message(CancelSessionState.session)
async def session_cancel_finish(message: Message, state: FSMContext):

    session = await get_session(int(message.text))

    if not session:

        await message.answer("❌ سانس پیدا نشد.")

        return

    await update_session(
        session.id,
        status="cancelled"
    )

    await state.clear()

    await message.answer("✅ سانس لغو شد.")

    # ==========================================================
# EDIT SESSION
# ==========================================================

@router.callback_query(F.data == "session_edit")
async def session_edit(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(EditSessionState.session)

    await callback.message.edit_text(
        "✏ شناسه سانس را ارسال کن."
    )


@router.message(EditSessionState.session)
async def session_edit_select(message: Message, state: FSMContext):

    session = await get_session(int(message.text))

    if not session:

        await message.answer(
            "❌ سانس پیدا نشد."
        )

        return

    await state.update_data(
        session_id=session.id
    )

    await state.set_state(EditSessionState.date)

    await message.answer(
        f"""📅 تاریخ فعلی:

{session.session_date}

تاریخ جدید را وارد کن."""
    )


@router.message(EditSessionState.date)
async def session_edit_date(message: Message, state: FSMContext):

    await state.update_data(
        date=message.text
    )

    await state.set_state(EditSessionState.time)

    await message.answer(
        "🕒 ساعت جدید را وارد کن."
    )


@router.message(EditSessionState.time)
async def session_edit_time(message: Message, state: FSMContext):

    await state.update_data(
        time=message.text
    )

    await state.set_state(EditSessionState.capacity)

    await message.answer(
        "👥 ظرفیت جدید را وارد کن."
    )


@router.message(EditSessionState.capacity)
async def session_edit_capacity(message: Message, state: FSMContext):

    await state.update_data(
        capacity=int(message.text)
    )

    await state.set_state(EditSessionState.price)

    await message.answer(
        "💰 قیمت جدید را وارد کن."
    )


@router.message(EditSessionState.price)
async def session_edit_price(message: Message, state: FSMContext):

    data = await state.get_data()

    await update_session(

        data["session_id"],

        session_date=data["date"],

        session_time=data["time"],

        capacity=data["capacity"],

        final_price=int(message.text),

    )

    await state.clear()

    await message.answer(
        "✅ اطلاعات سانس با موفقیت بروزرسانی شد."
    )


