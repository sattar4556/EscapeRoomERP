from aiogram.fsm.state import State

from aiogram.fsm.state import StatesGroup


class CRMState(

    StatesGroup,

):

    customer = State()

    phone = State()

    birthday = State()

    source = State()

    description = State()

    confirm = State()


class DiscountState(

    StatesGroup,

):

    customer = State()

    percent = State()

    expire_date = State()

    description = State()

    confirm = State()