from aiogram.fsm.state import State

from aiogram.fsm.state import StatesGroup


class StaffState(

    StatesGroup,

):

    full_name = State()

    phone = State()

    role = State()

    branch = State()

    salary = State()

    username = State()

    telegram_id = State()

    confirm = State()