from aiogram import Router
from aiogram import F

from aiogram.types import (
    CallbackQuery,
    Message,
)

from aiogram.fsm.context import FSMContext

from states.booking import BookingState

from database.crud import (
    get_session,
    get_game,
    create_booking,
)

from keyboards.main_menu import (
    back_menu,
)

router = Router()


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

    await state.update_data(
        session_id=session_id
    )

    await state.set_state(
        BookingState.customer_name
    )

    await callback.message.edit_text(
        """🎟 رزرو سانس

اسم رزرو کننده رو بفرست.

مثال:

ستار آقادادی"""
    )


@router.message(
    BookingState.customer_name
)
async def booking_name(
    message: Message,
    state: FSMContext,
):

    await state.update_data(
        customer_name=message.text
    )

    await state.set_state(
        BookingState.customer_phone
    )

    await message.answer(
        """📱 شماره موبایل رو ارسال کن.

مثال:

09123456789"""
    )


@router.message(
    BookingState.customer_phone
)
async def booking_phone(
    message: Message,
    state: FSMContext,
):

    await state.update_data(
        customer_phone=message.text
    )

    await state.set_state(
        BookingState.players_count
    )

    await message.answer(
        """👥 چند نفر هستید؟

فقط عدد ارسال کن.

مثال:

5"""
    )


@router.message(
    BookingState.players_count
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

    data = await state.get_data()

    session = await get_session(
        data["session_id"]
    )

    game = await get_game(
        session.game_id
    )

    total_price = (
        players *
        session.final_price
    )

    booking = await create_booking(

        session_id=session.id,

        user_id=message.from_user.id,

        customer_name=data["customer_name"],

        customer_phone=data["customer_phone"],

        players_count=players,

        total_price=total_price,

    )

    await state.clear()

    await message.answer(
f"""
🎉 رزروت با موفقیت ثبت شد.

━━━━━━━━━━━━━━

🎭 بازی

{game.title}

📅 تاریخ

{session.session_date}

⏰ ساعت

{session.session_time}

👥 تعداد نفرات

{players}

💰 مبلغ

{total_price:,} تومان

━━━━━━━━━━━━━━

🧾 کد رهگیری

{booking.booking_code}

منتظر دیدنت هستیم 😎
""",
        reply_markup=back_menu()
    )