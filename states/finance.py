from aiogram.fsm.state import State

from aiogram.fsm.state import StatesGroup


class IncomeState(

    StatesGroup,

):

    title = State()

    category = State()

    amount = State()

    payment_method = State()

    description = State()

    confirm = State()


class ExpenseState(

    StatesGroup,

):

    title = State()

    category = State()

    amount = State()

    payment_method = State()

    description = State()

    confirm = State()


class SalaryState(

    StatesGroup,

):

    staff = State()

    amount = State()

    month = State()

    description = State()

    confirm = State()