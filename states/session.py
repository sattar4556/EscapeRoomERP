from aiogram.fsm.state import State, StatesGroup


# ==========================================================
# ADD SESSION
# ==========================================================

class AddSessionState(StatesGroup):

    game = State()

    branch = State()

    date = State()

    time = State()

    capacity = State()

    price = State()

    confirm = State()


# ==========================================================
# EDIT SESSION
# ==========================================================

class EditSessionState(StatesGroup):

    session = State()

    menu = State()

    game = State()

    date = State()

    time = State()

    capacity = State()

    reserved = State()

    price = State()

    status = State()

    confirm = State()


# ==========================================================
# DELETE SESSION
# ==========================================================

class DeleteSessionState(StatesGroup):

    session = State()

    confirm = State()


# ==========================================================
# OPEN SESSION
# ==========================================================

class OpenSessionState(StatesGroup):

    session = State()


# ==========================================================
# CLOSE SESSION
# ==========================================================

class CloseSessionState(StatesGroup):

    session = State()


# ==========================================================
# CANCEL SESSION
# ==========================================================

class CancelSessionState(StatesGroup):

    session = State()


# ==========================================================
# SEARCH SESSION
# ==========================================================

class SearchSessionState(StatesGroup):

    date = State()

    game = State()


# ==========================================================
# COPY SESSION
# ==========================================================

class CopySessionState(StatesGroup):

    source = State()

    target_date = State()


# ==========================================================
# BULK CREATE SESSION
# ==========================================================

class BulkSessionState(StatesGroup):

    game = State()

    start_date = State()

    end_date = State()

    weekdays = State()

    times = State()

    capacity = State()

    price = State()

    confirm = State()