from database.crud import (
    dashboard_summary,
    dashboard_today,
    get_statistics,
    get_last_bookings,
    get_total_income,
    get_total_expense,
)


# ==========================================================
# DASHBOARD
# ==========================================================

async def dashboard():

    return await dashboard_summary()


# ==========================================================
# TODAY REPORT
# ==========================================================

async def today_report():

    sessions = await dashboard_today()

    return {

        "sessions": sessions,

        "count": len(sessions),

    }


# ==========================================================
# FINANCE REPORT
# ==========================================================

async def finance_report():

    income = await get_total_income()

    expense = await get_total_expense()

    return {

        "income": income,

        "expense": expense,

        "profit": income - expense,

    }


# ==========================================================
# BOOKING REPORT
# ==========================================================

async def booking_report():

    bookings = await get_last_bookings()

    return {

        "count": len(bookings),

        "items": bookings,

    }


# ==========================================================
# STATISTICS
# ==========================================================

async def statistics_report():

    return await get_statistics()


# ==========================================================
# FULL REPORT
# ==========================================================

async def full_report():

    dashboard_data = await dashboard()

    finance_data = await finance_report()

    booking_data = await booking_report()

    statistics_data = await statistics_report()

    return {

        "dashboard": dashboard_data,

        "finance": finance_data,

        "booking": booking_data,

        "statistics": statistics_data,

    }


# ==========================================================
# PROFIT
# ==========================================================

async def total_profit():

    income = await get_total_income()

    expense = await get_total_expense()

    return income - expense


# ==========================================================
# REPORT TEXT
# ==========================================================

async def dashboard_text():

    report = await full_report()

    return f"""
📊 داشبورد

💰 درآمد:
{report["finance"]["income"]:,}

💸 هزینه:
{report["finance"]["expense"]:,}

📈 سود:
{report["finance"]["profit"]:,}

📝 تعداد رزرو:
{report["booking"]["count"]}

👥 پرسنل:
{report["statistics"]["staff"]}

🎮 بازی:
{report["statistics"]["games"]}

📅 سانس:
{report["statistics"]["sessions"]}
"""