from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states.session import AddSession
from database.crud import (
    get_games,
    create_session,
)

router = Router()


@router.callback_query(F.data == "add_session")
async def add_session(callback: CallbackQuery, state: FSMContext):

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

    await state.set_state(AddSession.game)

    await callback.message.answer(
        text + "\n\nشماره بازی را وارد کن:"
    )


@router.message(AddSession.game)
async def session_game(message: Message, state: FSMContext):

    await state.update_data(
        game_id=int(message.text)
    )

    await state.set_state(AddSession.branch)

    await message.answer(
        "شماره شعبه:\n\nفعلاً 1 وارد کن."
    )


@router.message(AddSession.branch)
async def session_branch(message: Message, state: FSMContext):

    await state.update_data(
        branch_id=int(message.text)
    )

    await state.set_state(AddSession.date)

    await message.answer(
        "تاریخ:\n1405/05/10"
    )


@router.message(AddSession.date)
async def session_date(message: Message, state: FSMContext):

    await state.update_data(
        date=message.text
    )

    await state.set_state(AddSession.time)

    await message.answer(
        "ساعت:\n19:00"
    )


@router.message(AddSession.time)
async def session_time(message: Message, state: FSMContext):

    await state.update_data(
        time=message.text
    )

    await state.set_state(AddSession.capacity)

    await message.answer(
        "ظرفیت:"
    )


@router.message(AddSession.capacity)
async def session_capacity(message: Message, state: FSMContext):

    await state.update_data(
        capacity=int(message.text)
    )

    await state.set_state(AddSession.price)

    await message.answer(
        "قیمت:"
    )


@router.message(AddSession.price)
async def session_price(message: Message, state: FSMContext):

    data = await state.get_data()

    await create_session(
        game_id=data["game_id"],
        branch_id=data["branch_id"],
        session_date=data["date"],
        session_time=data["time"],
        capacity=data["capacity"],
        price=int(message.text),
    )

    await state.clear()

    await message.answer(
        "✅ سانس ثبت شد."
    )