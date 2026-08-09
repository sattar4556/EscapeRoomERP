from aiogram.fsm.state import State

from aiogram.fsm.state import StatesGroup


class NotificationState(

    StatesGroup,

):

    receiver = State()

    title = State()

    message = State()

    confirm = State()