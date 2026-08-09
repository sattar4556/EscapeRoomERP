from aiogram.fsm.state import State, StatesGroup


# ==========================================================
# ADD GAME
# ==========================================================

class AddGameState(StatesGroup):

    title = State()

    genre = State()

    difficulty = State()

    duration = State()

    min_players = State()

    max_players = State()

    base_price = State()

    holiday_price = State()

    weekend_price = State()

    age_limit = State()

    description = State()

    poster = State()

    trailer = State()

    confirm = State()


# ==========================================================
# EDIT GAME
# ==========================================================

class EditGameState(StatesGroup):

    select_game = State()

    menu = State()

    title = State()

    genre = State()

    difficulty = State()

    duration = State()

    min_players = State()

    max_players = State()

    base_price = State()

    holiday_price = State()

    weekend_price = State()

    age_limit = State()

    description = State()

    poster = State()

    trailer = State()

    confirm = State()


# ==========================================================
# DELETE GAME
# ==========================================================

class DeleteGameState(StatesGroup):

    select_game = State()

    confirm = State()


# ==========================================================
# ENABLE / DISABLE GAME
# ==========================================================

class EnableGameState(StatesGroup):

    select_game = State()


class DisableGameState(StatesGroup):

    select_game = State()


# ==========================================================
# SEARCH GAME
# ==========================================================

class SearchGameState(StatesGroup):

    keyword = State()


# ==========================================================
# FILTER GAME
# ==========================================================

class FilterGameState(StatesGroup):

    genre = State()

    difficulty = State()


# ==========================================================
# GAME IMAGE
# ==========================================================

class UploadPosterState(StatesGroup):

    game = State()

    image = State()


# ==========================================================
# GAME TRAILER
# ==========================================================

class UploadTrailerState(StatesGroup):

    game = State()

    video = State()