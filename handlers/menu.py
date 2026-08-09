from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.crud import get_games
from keyboards.main_menu import main_menu, back_menu

router = Router()


@router.callback_query(F.data == "home")
async def home(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        "🏠 منوی اصلی",
        reply_markup=main_menu()
    )


@router.callback_query(F.data == "booking")
async def booking(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        """🎟 رزرو سانس

🚧 این بخش در حال تکمیله...

به زودی میتونی:

✅ انتخاب بازی
✅ انتخاب تاریخ
✅ انتخاب ساعت
✅ ثبت رزرو
✅ پرداخت آنلاین

رو انجام بدی.""",
        reply_markup=back_menu()
    )


@router.callback_query(F.data == "games")
async def games(callback: CallbackQuery):

    await callback.answer()

    games = await get_games()

    if not games:

        await callback.message.edit_text(
            """🎭 بازی‌های مجموعه

هنوز هیچ بازی ثبت نشده.

مدیر مجموعه باید اول بازی‌ها رو اضافه کنه.""",
            reply_markup=back_menu()
        )

        return

    text = "🎭 بازی‌های مجموعه\n\n"

    for game in games:

        text += (
            f"🎲 {game.title}\n"
            f"🎭 ژانر: {game.genre}\n"
            f"👥 {game.min_players} تا {game.max_players} نفر\n"
            f"⏰ {game.duration} دقیقه\n"
            f"💰 {game.price:,} تومان\n\n"
        )

    await callback.message.edit_text(
        text,
        reply_markup=back_menu()
    )


@router.callback_query(F.data == "my_bookings")
async def my_bookings(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        """📅 رزروهای من

فعلاً هیچ رزروی ثبت نشده.

بعد از اولین رزرو، لیستش اینجا نمایش داده میشه.""",
        reply_markup=back_menu()
    )


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):

    await callback.answer()

    user = callback.from_user

    await callback.message.edit_text(
        f"""👤 پروفایل

🆔 شناسه: {user.id}

👤 نام:
{user.full_name}

📛 یوزرنیم:
@{user.username if user.username else "ندارد"}

🎭 نقش:
مشتری

📅 تعداد رزروها:
0

🔥 امتیاز باشگاه مشتریان:
0""",
        reply_markup=back_menu()
    )


@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        """☎️ پشتیبانی

اگر سوال یا مشکلی داشتی با ما در ارتباط باش.

📞 09991206120

📞 09991207120

📞 09991208120""",
        reply_markup=back_menu()
    )