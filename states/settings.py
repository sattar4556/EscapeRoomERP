from aiogram.fsm.state import State

from aiogram.fsm.state import StatesGroup


class SettingsState(

    StatesGroup,

):

    organization_name = State()

    phone = State()

    address = State()

    instagram = State()

    website = State()

    description = State()

    confirm = State()