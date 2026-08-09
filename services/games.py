from database.crud import (
    get_games,
    get_game,
)


async def all_games():

    return await get_games()


async def one_game(game_id):

    return await get_game(game_id)