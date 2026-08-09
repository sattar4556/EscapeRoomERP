from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud import get_games


async def games_menu():

    kb = InlineKeyboardBuilder()

    games = await get_games()

    for game in games:

        kb.button(
            text=game.title,
            callback_data=f"game_{game.id}"
        )

    kb.button(
        text="🔙 بازگشت",
        callback_data="home"
    )

    kb.adjust(1)

    return kb.as_markup()