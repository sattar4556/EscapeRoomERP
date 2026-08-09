from aiogram.fsm.state import State

from aiogram.fsm.state import StatesGroup


class InventoryState(

    StatesGroup,

):

    item_name = State()

    category = State()

    brand = State()

    unit = State()

    quantity = State()

    minimum_quantity = State()

    purchase_price = State()

    sale_price = State()

    supplier = State()

    description = State()

    confirm = State()


class StockInState(

    StatesGroup,

):

    item = State()

    quantity = State()

    price = State()

    invoice = State()

    description = State()

    confirm = State()


class StockOutState(

    StatesGroup,

):

    item = State()

    quantity = State()

    reason = State()

    description = State()

    confirm = State()
    