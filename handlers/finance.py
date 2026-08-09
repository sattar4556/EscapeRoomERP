from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.crud import (
    create_income,
    create_expense,
    get_staff,
    pay_salary,
)

from states.finance import (
    AddIncomeState,
    AddExpenseState,
    SalaryState,
)

router = Router()


# ==========================================================
# ADD INCOME
# ==========================================================

@router.callback_query(F.data == "finance_income")
async def finance_income(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(AddIncomeState.title)

    await callback.message.edit_text(
        "💰 عنوان درآمد را وارد کن."
    )


@router.message(AddIncomeState.title)
async def income_title(message: Message, state: FSMContext):

    await state.update_data(
        title=message.text
    )

    await state.set_state(AddIncomeState.category)

    await message.answer(
        "📂 دسته درآمد را وارد کن."
    )


@router.message(AddIncomeState.category)
async def income_category(message: Message, state: FSMContext):

    await state.update_data(
        category=message.text
    )

    await state.set_state(AddIncomeState.amount)

    await message.answer(
        "💵 مبلغ را وارد کن."
    )


@router.message(AddIncomeState.amount)
async def income_amount(message: Message, state: FSMContext):

    await state.update_data(
        amount=int(message.text)
    )

    await state.set_state(AddIncomeState.payment_method)

    await message.answer(
        """روش پرداخت

cash

card

online"""
    )


@router.message(AddIncomeState.payment_method)
async def income_method(message: Message, state: FSMContext):

    await state.update_data(
        payment_method=message.text
    )

    await state.set_state(AddIncomeState.description)

    await message.answer(
        "📝 توضیحات"
    )


@router.message(AddIncomeState.description)
async def income_finish(message: Message, state: FSMContext):

    data = await state.get_data()

    await create_income(

        title=data["title"],

        category=data["category"],

        amount=data["amount"],

        payment_method=data["payment_method"],

        description=message.text,

    )

    await state.clear()

    await message.answer(
        "✅ درآمد ثبت شد."
    )


# ==========================================================
# ADD EXPENSE
# ==========================================================

@router.callback_query(F.data == "finance_expense")
async def finance_expense(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(AddExpenseState.title)

    await callback.message.edit_text(
        "💸 عنوان هزینه را وارد کن."
    )


@router.message(AddExpenseState.title)
async def expense_title(message: Message, state: FSMContext):

    await state.update_data(
        title=message.text
    )

    await state.set_state(AddExpenseState.category)

    await message.answer(
        "📂 دسته هزینه را وارد کن."
    )


@router.message(AddExpenseState.category)
async def expense_category(message: Message, state: FSMContext):

    await state.update_data(
        category=message.text
    )

    await state.set_state(AddExpenseState.amount)

    await message.answer(
        "💵 مبلغ هزینه را وارد کن."
    )


@router.message(AddExpenseState.amount)
async def expense_amount(message: Message, state: FSMContext):

    await state.update_data(
        amount=int(message.text)
    )

    await state.set_state(AddExpenseState.payment_method)

    await message.answer(
        """روش پرداخت

cash

card

online"""
    )


@router.message(AddExpenseState.payment_method)
async def expense_method(message: Message, state: FSMContext):

    await state.update_data(
        payment_method=message.text
    )

    await state.set_state(AddExpenseState.description)

    await message.answer(
        "📝 توضیحات"
    )


@router.message(AddExpenseState.description)
async def expense_finish(message: Message, state: FSMContext):

    data = await state.get_data()

    await create_expense(

        title=data["title"],

        category=data["category"],

        amount=data["amount"],

        payment_method=data["payment_method"],

        description=message.text,

    )

    await state.clear()

    await message.answer(
        "✅ هزینه ثبت شد."
    )


# ==========================================================
# PAY SALARY
# ==========================================================

@router.callback_query(F.data == "finance_salary")
async def finance_salary(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    staffs = await get_staff()

    if not staffs:

        await callback.message.edit_text(
            "❌ هیچ پرسنلی ثبت نشده است."
        )

        return

    text = "👨‍💼 شناسه پرسنل را انتخاب کن.\n\n"

    for staff in staffs:

        text += (
            f"{staff.id} - "
            f"{staff.name} "
            f"({staff.role})\n"
        )

    await state.set_state(SalaryState.staff)

    await callback.message.edit_text(text)


@router.message(SalaryState.staff)
async def salary_staff(message: Message, state: FSMContext):

    await state.update_data(
        staff_id=int(message.text)
    )

    await state.set_state(
        SalaryState.amount
    )

    await message.answer(
        "💰 مبلغ حقوق را وارد کن."
    )


@router.message(SalaryState.amount)
async def salary_amount(message: Message, state: FSMContext):

    await state.update_data(
        amount=int(message.text)
    )

    await state.set_state(
        SalaryState.month
    )

    await message.answer(
        "📅 ماه پرداخت را وارد کن.\n\nمثال:\n1405/05"
    )


@router.message(SalaryState.month)
async def salary_month(message: Message, state: FSMContext):

    await state.update_data(
        month=message.text
    )

    await state.set_state(
        SalaryState.description
    )

    await message.answer(
        "📝 توضیحات پرداخت را وارد کن.\n\nاگر ندارد '-' ارسال کن."
    )


@router.message(SalaryState.description)
async def salary_finish(message: Message, state: FSMContext):

    data = await state.get_data()

    await pay_salary(

        staff_id=data["staff_id"],

        amount=data["amount"],

        month=data["month"],

        description=message.text,

    )

    await state.clear()

    await message.answer(
        "✅ حقوق با موفقیت پرداخت و ثبت شد."
    )


# ==========================================================
# FINANCE DASHBOARD
# ==========================================================

@router.callback_query(F.data == "finance_dashboard")
async def finance_dashboard(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(

        """💰 داشبورد مالی

📈 درآمد امروز

📉 هزینه امروز

💵 موجودی صندوق

🏦 موجودی حساب بانکی

👨‍💼 حقوق پرداخت نشده

📊 سود خالص

(در مرحله بعد به دیتابیس متصل می‌شود.)"""

    )


from database.crud import (
    get_today_income,
    get_today_expense,
    get_cash_balance,
    get_bank_balance,
    get_total_income,
    get_total_expense,
    get_unpaid_salary,
)


# ==========================================================
# TODAY REPORT
# ==========================================================

@router.callback_query(F.data == "finance_today")
async def finance_today(callback: CallbackQuery):

    await callback.answer()

    income = await get_today_income()

    expense = await get_today_expense()

    profit = income - expense

    await callback.message.edit_text(

        f"""📅 گزارش امروز

💰 درآمد:
{income:,}

💸 هزینه:
{expense:,}

📈 سود:
{profit:,}"""

    )


# ==========================================================
# CASH REPORT
# ==========================================================

@router.callback_query(F.data == "finance_cash")
async def finance_cash(callback: CallbackQuery):

    await callback.answer()

    cash = await get_cash_balance()

    await callback.message.edit_text(

        f"""💵 صندوق

موجودی فعلی:

{cash:,}"""

    )


# ==========================================================
# BANK REPORT
# ==========================================================

@router.callback_query(F.data == "finance_bank")
async def finance_bank(callback: CallbackQuery):

    await callback.answer()

    bank = await get_bank_balance()

    await callback.message.edit_text(

        f"""🏦 حساب بانکی

موجودی فعلی:

{bank:,}"""

    )


# ==========================================================
# TOTAL REPORT
# ==========================================================

@router.callback_query(F.data == "finance_total")
async def finance_total(callback: CallbackQuery):

    await callback.answer()

    income = await get_total_income()

    expense = await get_total_expense()

    profit = income - expense

    await callback.message.edit_text(

        f"""📊 گزارش کلی

💰 کل درآمد

{income:,}

💸 کل هزینه

{expense:,}

📈 سود خالص

{profit:,}"""

    )


# ==========================================================
# UNPAID SALARY
# ==========================================================

@router.callback_query(F.data == "finance_unpaid_salary")
async def unpaid_salary(callback: CallbackQuery):

    await callback.answer()

    staffs = await get_unpaid_salary()

    if not staffs:

        await callback.message.edit_text(

            "✅ هیچ حقوق پرداخت نشده‌ای وجود ندارد."

        )

        return

    text = "👨‍💼 حقوق پرداخت نشده\n\n"

    for staff in staffs:

        text += (

            f"{staff.name}\n"

            f"{staff.salary:,}\n\n"

        )

    await callback.message.edit_text(text)


