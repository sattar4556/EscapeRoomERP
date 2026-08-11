from aiogram.fsm.state import State, StatesGroup


# ==========================================================
# ADD SESSION
# ==========================================================

class AddSession(StatesGroup):
    game = State()
    branch = State()
    date = State()
    time = State()
    capacity = State()
    price = State()