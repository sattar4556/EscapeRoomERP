from aiogram.fsm.state import State

from aiogram.fsm.state import StatesGroup


class BookingState(

    StatesGroup,

):

    select_game = State()

    select_session = State()

    customer_name = State()

    customer_phone = State()

    players = State()

    discount = State()

    total_price = State()

    paid_amount = State()

    payment_method = State()

    description = State()

    confirm = State()