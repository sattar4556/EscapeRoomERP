from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.crud import (
    create_staff,
    get_staff,
    get_staff_member,
    update_staff,
    delete_staff,
)

from states.staff import (
    AddStaffState,
    EditStaffState,
    DeleteStaffState,
)

router = Router()


# ==========================================================
# ADD STAFF
# ==========================================================

@router.callback_query(F.data == "admin_staff")
async def staff_menu(callback: CallbackQuery):

    await callback.answer()

    await callback.message.edit_text(
        """👨‍💼 مدیریت پرسنل

1️⃣ افزودن پرسنل

2️⃣ لیست پرسنل

3️⃣ ویرایش

4️⃣ حذف

برای شروع روی یکی از گزینه‌ها کلیک کن."""
    )


@router.callback_query(F.data == "staff_add")
async def staff_add(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(AddStaffState.name)

    await callback.message.edit_text(
        "👤 نام و نام خانوادگی پرسنل را وارد کن."
    )


@router.message(AddStaffState.name)
async def staff_name(message: Message, state: FSMContext):

    await state.update_data(
        name=message.text
    )

    await state.set_state(AddStaffState.phone)

    await message.answer(
        "📱 شماره موبایل را وارد کن."
    )


@router.message(AddStaffState.phone)
async def staff_phone(message: Message, state: FSMContext):

    await state.update_data(
        phone=message.text
    )

    await state.set_state(AddStaffState.role)

    await message.answer(
        """🎭 سمت را وارد کن.

admin

gm

actor

cashier

accountant"""
    )


@router.message(AddStaffState.role)
async def staff_role(message: Message, state: FSMContext):

    await state.update_data(
        role=message.text.lower()
    )

    await state.set_state(AddStaffState.salary)

    await message.answer(
        "💰 حقوق را وارد کن."
    )


@router.message(AddStaffState.salary)
async def staff_salary(message: Message, state: FSMContext):

    data = await state.get_data()

    await create_staff(

        name=data["name"],

        phone=data["phone"],

        role=data["role"],

        salary=int(message.text),

    )

    await state.clear()

    await message.answer(
        "✅ پرسنل با موفقیت ثبت شد."
    )


# ==========================================================
# STAFF LIST
# ==========================================================

@router.callback_query(F.data == "staff_list")
async def staff_list(callback: CallbackQuery):

    await callback.answer()

    staffs = await get_staff()

    if not staffs:

        await callback.message.edit_text(
            "❌ هیچ پرسنلی ثبت نشده."
        )

        return

    text = "👨‍💼 لیست پرسنل\n\n"

    for staff in staffs:

        text += (
            f"🆔 {staff.id}\n"
            f"👤 {staff.name}\n"
            f"🎭 {staff.role}\n"
            f"📱 {staff.phone}\n"
            f"💰 {staff.salary:,}\n\n"
        )

    await callback.message.edit_text(text)


# ==========================================================
# EDIT STAFF
# ==========================================================

@router.callback_query(F.data == "staff_edit")
async def staff_edit(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(EditStaffState.staff)

    await callback.message.edit_text(
        "✏ شناسه پرسنل را ارسال کن."
    )


@router.message(EditStaffState.staff)
async def staff_edit_select(message: Message, state: FSMContext):

    staff = await get_staff_member(int(message.text))

    if not staff:

        await message.answer(
            "❌ پرسنل پیدا نشد."
        )

        return

    await state.update_data(
        staff_id=staff.id
    )

    await state.set_state(
        EditStaffState.name
    )

    await message.answer(
        f"""👤 نام فعلی:

{staff.name}

نام جدید را ارسال کن."""
    )


@router.message(EditStaffState.name)
async def staff_edit_name(message: Message, state: FSMContext):

    await state.update_data(
        name=message.text
    )

    await state.set_state(
        EditStaffState.phone
    )

    await message.answer(
        "📱 شماره جدید را وارد کن."
    )


@router.message(EditStaffState.phone)
async def staff_edit_phone(message: Message, state: FSMContext):

    await state.update_data(
        phone=message.text
    )

    await state.set_state(
        EditStaffState.role
    )

    await message.answer(
        "🎭 سمت جدید را وارد کن."
    )


@router.message(EditStaffState.role)
async def staff_edit_role(message: Message, state: FSMContext):

    await state.update_data(
        role=message.text.lower()
    )

    await state.set_state(
        EditStaffState.salary
    )

    await message.answer(
        "💰 حقوق جدید را وارد کن."
    )


@router.message(EditStaffState.salary)
async def staff_edit_salary(message: Message, state: FSMContext):

    data = await state.get_data()

    await update_staff(

        data["staff_id"],

        name=data["name"],

        phone=data["phone"],

        role=data["role"],

        salary=int(message.text),

    )

    await state.clear()

    await message.answer(
        "✅ اطلاعات پرسنل بروزرسانی شد."
    )


# ==========================================================
# DELETE STAFF
# ==========================================================

@router.callback_query(F.data == "staff_delete")
async def staff_delete(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(
        DeleteStaffState.staff
    )

    await callback.message.edit_text(
        "🗑 شناسه پرسنل را ارسال کن."
    )


@router.message(DeleteStaffState.staff)
async def staff_delete_finish(message: Message, state: FSMContext):

    staff = await get_staff_member(int(message.text))

    if not staff:

        await message.answer(
            "❌ پرسنل پیدا نشد."
        )

        return

    await delete_staff(staff.id)

    await state.clear()

    await message.answer(
        "✅ پرسنل حذف شد."
    )


# ==========================================================
# CHANGE ROLE
# ==========================================================

@router.callback_query(F.data == "staff_change_role")
async def change_role(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(
        ChangeRoleState.staff
    )

    await callback.message.edit_text(
        "🆔 شناسه پرسنل را ارسال کن."
    )


@router.message(ChangeRoleState.staff)
async def change_role_select(message: Message, state: FSMContext):

    await state.update_data(
        staff_id=int(message.text)
    )

    await state.set_state(
        ChangeRoleState.role
    )

    await message.answer(
        "🎭 سمت جدید را وارد کن."
    )


@router.message(ChangeRoleState.role)
async def change_role_finish(message: Message, state: FSMContext):

    data = await state.get_data()

    await update_staff(

        data["staff_id"],

        role=message.text.lower(),

    )

    await state.clear()

    await message.answer(
        "✅ سمت پرسنل تغییر کرد."
    )


# ==========================================================
# CHANGE SALARY
# ==========================================================

@router.callback_query(F.data == "staff_change_salary")
async def change_salary(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(
        ChangeSalaryState.staff
    )

    await callback.message.edit_text(
        "🆔 شناسه پرسنل را ارسال کن."
    )


@router.message(ChangeSalaryState.staff)
async def change_salary_select(message: Message, state: FSMContext):

    staff = await get_staff_member(
        int(message.text)
    )

    if not staff:

        await message.answer(
            "❌ پرسنل پیدا نشد."
        )

        return

    await state.update_data(
        staff_id=staff.id
    )

    await state.set_state(
        ChangeSalaryState.salary
    )

    await message.answer(
        f"""💰 حقوق فعلی:

{staff.salary:,}

حقوق جدید را وارد کن."""
    )


@router.message(ChangeSalaryState.salary)
async def change_salary_finish(message: Message, state: FSMContext):

    data = await state.get_data()

    await update_staff(

        data["staff_id"],

        salary=int(message.text),

    )

    await state.clear()

    await message.answer(
        "✅ حقوق پرسنل بروزرسانی شد."
    )


# ==========================================================
# ENABLE STAFF
# ==========================================================

@router.callback_query(F.data == "staff_enable")
async def enable_staff(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(
        EnableStaffState.staff
    )

    await callback.message.edit_text(
        "✅ شناسه پرسنل را ارسال کن."
    )


@router.message(EnableStaffState.staff)
async def enable_staff_finish(message: Message, state: FSMContext):

    staff = await get_staff_member(
        int(message.text)
    )

    if not staff:

        await message.answer(
            "❌ پرسنل پیدا نشد."
        )

        return

    await update_staff(

        staff.id,

        is_active=True,

    )

    await state.clear()

    await message.answer(
        "✅ پرسنل فعال شد."
    )


# ==========================================================
# DISABLE STAFF
# ==========================================================

@router.callback_query(F.data == "staff_disable")
async def disable_staff(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.set_state(
        DisableStaffState.staff
    )

    await callback.message.edit_text(
        "🚫 شناسه پرسنل را ارسال کن."
    )


@router.message(DisableStaffState.staff)
async def disable_staff_finish(message: Message, state: FSMContext):

    staff = await get_staff_member(
        int(message.text)
    )

    if not staff:

        await message.answer(
            "❌ پرسنل پیدا نشد."
        )

        return

    await update_staff(

        staff.id,

        is_active=False,

    )

    await state.clear()

    await message.answer(
        "🚫 پرسنل غیرفعال شد."
    )


