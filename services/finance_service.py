from database.crud import (
    create_income,
    create_expense,
    pay_salary,
    get_cash_balance,
    get_bank_balance,
    get_total_income,
    get_total_expense,
)


# ==========================================================
# INCOME
# ==========================================================

async def add_income(

    title,

    category,

    amount,

    payment_method,

    description="",

):

    return await create_income(

        title=title,

        category=category,

        amount=amount,

        payment_method=payment_method,

        description=description,

    )


# ==========================================================
# EXPENSE
# ==========================================================

async def add_expense(

    title,

    category,

    amount,

    payment_method,

    description="",

):

    return await create_expense(

        title=title,

        category=category,

        amount=amount,

        payment_method=payment_method,

        description=description,

    )


# ==========================================================
# SALARY
# ==========================================================

async def salary_payment(

    staff_id,

    amount,

    month,

    description="",

):

    return await pay_salary(

        staff_id=staff_id,

        amount=amount,

        month=month,

        description=description,

    )


# ==========================================================
# CASH
# ==========================================================

async def cash_balance():

    return await get_cash_balance()


# ==========================================================
# BANK
# ==========================================================

async def bank_balance():

    return await get_bank_balance()


# ==========================================================
# PROFIT
# ==========================================================

async def profit():

    income = await get_total_income()

    expense = await get_total_expense()

    return income - expense


# ==========================================================
# DASHBOARD
# ==========================================================

async def finance_dashboard():

    income = await get_total_income()

    expense = await get_total_expense()

    cash = await get_cash_balance()

    bank = await get_bank_balance()

    return {

        "income": income,

        "expense": expense,

        "profit": income - expense,

        "cash": cash,

        "bank": bank,

    }


# ==========================================================
# CHECK PAYMENT
# ==========================================================

async def payment_completed(

    paid_amount,

    total_amount,

):

    return paid_amount >= total_amount