from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.crud import (
    create_game,
    get_games,
    get_game,
    update_game,
    delete_game,
)

from states.game import AddGameState

router = Router()


# ==========================================================
# ADD GAME
# ==========================================================

@router.callback_query(F.data == "game_add")
async def game_add(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(AddGameState.title)

    await callback.message.edit_text(

        """🎮 افزودن بازی

اسم بازی رو ارسال کن.

مثال:

پیمان عزازیل"""

    )


@router.message(AddGameState.title)
async def game_title(message: Message, state: FSMContext):

    await state.update_data(
        title=message.text
    )

    await state.set_state(AddGameState.genre)

    await message.answer(

        """🎭 ژانر بازی؟

مثال:

ترسناک
معمایی
روانشناختی"""

    )


@router.message(AddGameState.genre)
async def game_genre(message: Message, state: FSMContext):

    await state.update_data(
        genre=message.text
    )

    await state.set_state(
        AddGameState.difficulty
    )

    await message.answer(

        """🧠 درجه سختی؟

مثال:

1
2
3
4
5"""

    )


@router.message(AddGameState.difficulty)
async def game_difficulty(message: Message, state: FSMContext):

    await state.update_data(

        difficulty=int(message.text)

    )

    await state.set_state(
        AddGameState.duration
    )

    await message.answer(

        "⏱ مدت بازی؟ (دقیقه)"

    )


@router.message(AddGameState.duration)
async def game_duration(message: Message, state: FSMContext):

    await state.update_data(

        duration=int(message.text)

    )

    await state.set_state(
        AddGameState.min_players
    )

    await message.answer(

        "👤 حداقل نفرات؟"

    )


@router.message(AddGameState.min_players)
async def game_min(message: Message, state: FSMContext):

    await state.update_data(

        min_players=int(message.text)

    )

    await state.set_state(
        AddGameState.max_players
    )

    await message.answer(

        "👥 حداکثر نفرات؟"

    )


@router.message(AddGameState.max_players)
async def game_max(message: Message, state: FSMContext):

    await state.update_data(

        max_players=int(message.text)

    )

    await state.set_state(
        AddGameState.base_price
    )

    await message.answer(

        "💰 قیمت عادی (تومان)"

    )
    @router.message(AddGameState.base_price)
async def game_price(message: Message, state: FSMContext):

    await state.update_data(

        base_price=int(message.text)

    )

    await state.set_state(
        AddGameState.holiday_price
    )

    await message.answer(

        "🎉 قیمت روزهای تعطیل؟"

    )


@router.message(AddGameState.holiday_price)
async def game_holiday_price(message: Message, state: FSMContext):

    await state.update_data(

        holiday_price=int(message.text)

    )

    await state.set_state(
        AddGameState.weekend_price
    )

    await message.answer(

        "📅 قیمت آخر هفته؟"

    )


@router.message(AddGameState.weekend_price)
async def game_weekend_price(message: Message, state: FSMContext):

    await state.update_data(

        weekend_price=int(message.text)

    )

    await state.set_state(
        AddGameState.age_limit
    )

    await message.answer(

        "🔞 محدودیت سنی؟"

    )


@router.message(AddGameState.age_limit)
async def game_age(message: Message, state: FSMContext):

    await state.update_data(

        age_limit=int(message.text)

    )

    await state.set_state(
        AddGameState.description
    )

    await message.answer(

        "📝 توضیحات بازی را ارسال کن."

    )


@router.message(AddGameState.description)
async def game_description(message: Message, state: FSMContext):

    await state.update_data(

        description=message.text

    )

    data = await state.get_data()

    await create_game(

        organization_id=1,

        title=data["title"],

        genre=data["genre"],

        difficulty=data["difficulty"],

        duration=data["duration"],

        min_players=data["min_players"],

        max_players=data["max_players"],

        base_price=data["base_price"],

        holiday_price=data["holiday_price"],

        weekend_price=data["weekend_price"],

        age_limit=data["age_limit"],

        description=data["description"],

    )

    await state.clear()

    await message.answer(

        """✅ بازی با موفقیت ثبت شد.

از پنل مدیریت میتونی ویرایش یا حذفش کنی."""

    )


# ==========================================================
# GAME LIST
# ==========================================================

@router.callback_query(F.data == "game_list")
async def game_list(callback: CallbackQuery):

    await callback.answer()

    games = await get_games()

    if not games:

        await callback.message.edit_text(

            "❌ هیچ بازی ثبت نشده."

        )

        return

    text = "🎮 لیست بازی‌ها\n\n"

    for game in games:

        text += (

            f"🆔 {game.id}\n"

            f"🎭 {game.title}\n"

            f"📚 ژانر: {game.genre}\n"

            f"👥 {game.min_players} تا {game.max_players} نفر\n"

            f"⏱ {game.duration} دقیقه\n"

            f"💰 {game.base_price:,} تومان\n\n"

        )

    await callback.message.edit_text(text)
    from states.game import (
    EditGameState,
    DeleteGameState,
    EnableGameState,
    DisableGameState,
)

# ==========================================================
# DELETE GAME
# ==========================================================

@router.callback_query(F.data == "game_delete")
async def delete_game_start(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(DeleteGameState.select_game)

    await callback.message.edit_text(

        "🗑 شناسه بازی را ارسال کن."

    )


@router.message(DeleteGameState.select_game)
async def delete_game_finish(message: Message, state: FSMContext):

    game = await get_game(int(message.text))

    if not game:

        await message.answer(

            "❌ بازی پیدا نشد."

        )

        return

    await delete_game(game.id)

    await state.clear()

    await message.answer(

        "✅ بازی با موفقیت حذف شد."

    )


# ==========================================================
# ENABLE GAME
# ==========================================================

@router.callback_query(F.data == "game_enable")
async def enable_game(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(
        EnableGameState.select_game
    )

    await callback.message.edit_text(

        "✅ شناسه بازی را ارسال کن."

    )


@router.message(EnableGameState.select_game)
async def enable_game_finish(message: Message, state: FSMContext):

    game = await get_game(int(message.text))

    if not game:

        await message.answer("❌ بازی پیدا نشد.")

        return

    await update_game(

        game.id,

        is_active=True,

    )

    await state.clear()

    await message.answer(

        "✅ بازی فعال شد."

    )


# ==========================================================
# DISABLE GAME
# ==========================================================

@router.callback_query(F.data == "game_disable")
async def disable_game(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(

        DisableGameState.select_game

    )

    await callback.message.edit_text(

        "🚫 شناسه بازی را ارسال کن."

    )


@router.message(DisableGameState.select_game)
async def disable_game_finish(message: Message, state: FSMContext):

    game = await get_game(int(message.text))

    if not game:

        await message.answer(

            "❌ بازی پیدا نشد."

        )

        return

    await update_game(

        game.id,

        is_active=False,

    )

    await state.clear()

    await message.answer(

        "🚫 بازی غیرفعال شد."

    )


# ==========================================================
# EDIT GAME
# ==========================================================

@router.callback_query(F.data == "game_edit")
async def edit_game(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(

        EditGameState.select_game

    )

    await callback.message.edit_text(

        "✏ شناسه بازی را ارسال کن."

    )


@router.message(EditGameState.select_game)
async def edit_game_select(message: Message, state: FSMContext):

    game = await get_game(int(message.text))

    if not game:

        await message.answer(

            "❌ بازی پیدا نشد."

        )

        return

    await state.update_data(

        game_id=game.id

    )

    await state.set_state(

        EditGameState.title

    )

    await message.answer(

        f"""🎮 نام فعلی:

{game.title}

نام جدید را ارسال کن."""

    )


@router.message(EditGameState.title)
async def edit_game_title(message: Message, state: FSMContext):

    data = await state.get_data()

    await update_game(

        data["game_id"],

        title=message.text,

    )

    await state.clear()

    await message.answer(

        "✅ نام بازی بروزرسانی شد."

    )