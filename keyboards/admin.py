from aiogram.utils.keyboard import InlineKeyboardBuilder


# ==========================================================
# ADMIN MENU
# ==========================================================

def admin_menu():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🎮 مدیریت بازی‌ها",
        callback_data="admin_games"
    )

    kb.button(
        text="📅 مدیریت سانس‌ها",
        callback_data="admin_sessions"
    )

    kb.button(
        text="🎟 مدیریت رزروها",
        callback_data="admin_bookings"
    )

    kb.button(
        text="👥 مدیریت کاربران",
        callback_data="admin_users"
    )

    kb.button(
        text="👨‍💼 مدیریت پرسنل",
        callback_data="admin_staff"
    )

    kb.button(
        text="💰 امور مالی",
        callback_data="admin_finance"
    )

    kb.button(
        text="📦 انبار",
        callback_data="admin_inventory"
    )

    kb.button(
        text="🎁 باشگاه مشتریان",
        callback_data="admin_club"
    )

    kb.button(
        text="📊 گزارشات",
        callback_data="admin_reports"
    )

    kb.button(
        text="⚙ تنظیمات",
        callback_data="admin_settings"
    )

    kb.button(
        text="🏠 منوی اصلی",
        callback_data="home"
    )

    kb.adjust(2,2,2,2,2,1)

    return kb.as_markup()


# ==========================================================
# GAMES MENU
# ==========================================================

def games_admin_menu():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="➕ افزودن بازی",
        callback_data="game_add"
    )

    kb.button(
        text="📋 لیست بازی‌ها",
        callback_data="game_list"
    )

    kb.button(
        text="✏ ویرایش بازی",
        callback_data="game_edit"
    )

    kb.button(
        text="🗑 حذف بازی",
        callback_data="game_delete"
    )

    kb.button(
        text="✅ فعال کردن",
        callback_data="game_enable"
    )

    kb.button(
        text="🚫 غیرفعال کردن",
        callback_data="game_disable"
    )

    kb.button(
        text="🔙 بازگشت",
        callback_data="admin"
    )

    kb.adjust(2,2,2,1)

    return kb.as_markup()


# ==========================================================
# SESSIONS MENU
# ==========================================================

def sessions_admin_menu():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="➕ افزودن سانس",
        callback_data="session_add"
    )

    kb.button(
        text="📋 لیست سانس‌ها",
        callback_data="session_list"
    )

    kb.button(
        text="✏ ویرایش",
        callback_data="session_edit"
    )

    kb.button(
        text="🗑 حذف",
        callback_data="session_delete"
    )

    kb.button(
        text="🔓 باز کردن",
        callback_data="session_open"
    )

    kb.button(
        text="🔒 بستن",
        callback_data="session_close"
    )

    kb.button(
        text="❌ لغو سانس",
        callback_data="session_cancel"
    )

    kb.button(
        text="🔙 بازگشت",
        callback_data="admin"
    )

    kb.adjust(2,2,2,1,1)

    return kb.as_markup()


# ==========================================================
# USERS MENU
# ==========================================================

def users_admin_menu():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="📋 لیست کاربران",
        callback_data="users_list"
    )

    kb.button(
        text="🔍 جستجو",
        callback_data="users_search"
    )

    kb.button(
        text="🚫 مسدود",
        callback_data="users_ban"
    )

    kb.button(
        text="✅ رفع مسدودی",
        callback_data="users_unban"
    )

    kb.button(
        text="⭐ تغییر سطح",
        callback_data="users_role"
    )

    kb.button(
        text="💰 کیف پول",
        callback_data="users_wallet"
    )

    kb.button(
        text="🎁 امتیاز",
        callback_data="users_points"
    )

    kb.button(
        text="🔙 بازگشت",
        callback_data="admin"
    )

    kb.adjust(2,2,2,1,1)

    return kb.as_markup()


# ==========================================================
# REPORTS MENU
# ==========================================================

def reports_admin_menu():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="💰 فروش امروز",
        callback_data="report_today"
    )

    kb.button(
        text="📅 فروش ماه",
        callback_data="report_month"
    )

    kb.button(
        text="🎟 رزروها",
        callback_data="report_booking"
    )

    kb.button(
        text="👥 کاربران",
        callback_data="report_users"
    )

    kb.button(
        text="🎮 بازی‌ها",
        callback_data="report_games"
    )

    kb.button(
        text="📈 آمار کلی",
        callback_data="report_dashboard"
    )

    kb.button(
        text="📄 خروجی Excel",
        callback_data="report_excel"
    )

    kb.button(
        text="📄 خروجی PDF",
        callback_data="report_pdf"
    )

    kb.button(
        text="🔙 بازگشت",
        callback_data="admin"
    )

    kb.adjust(2,2,2,2,1)

    return kb.as_markup()