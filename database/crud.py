from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from database.database import SessionLocal
from database.models import User, Role, UserRole, Game, Session, Booking, BookingPayment


async def get_user(telegram_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()


async def create_or_update_user(
    telegram_id: int,
    username: str | None,
    first_name: str,
    last_name: str | None,
):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user:
            user.login_count += 1
            user.last_login = datetime.utcnow()
            if username:
                user.username = username
            user.first_name = first_name
            user.last_name = last_name
            await session.commit()
            await session.refresh(user)
            return user, False

        user = User(
            organization_id=1,
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            login_count=1,
            last_login=datetime.utcnow(),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user, True


# --- Game Functions ---

async def get_games():
    """Returns all active games"""
    async with SessionLocal() as session:
        result = await session.execute(select(Game).where(Game.is_active == True))
        return result.scalars().all()

# Aliases for compatibility
get_all_games = get_games


async def get_game_by_id(game_id: int):
    async with SessionLocal() as session:
        result = await session.execute(select(Game).where(Game.id == game_id))
        return result.scalar_one_or_none()

# Aliases for compatibility
get_game = get_game_by_id


async def get_available_sessions(game_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Session).where(Session.game_id == game_id, Session.is_active == True)
        )
        return result.scalars().all()

# Aliases for compatibility
get_game_sessions = get_available_sessions


# --- Booking Functions ---

async def get_booking(booking_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Booking)
            .options(selectinload(Booking.session).selectinload(Session.game), selectinload(Booking.payments))
            .where(Booking.id == booking_id)
        )
        return result.scalar_one_or_none()

# ==========================================================
# PAYMENT FUNCTIONS
# ==========================================================

async def get_booking_paid_amount(
    booking_id: int,
):
    async with SessionLocal() as session:

        result = await session.execute(
            select(
                func.sum(BookingPayment.amount)
            ).where(
                BookingPayment.booking_id == booking_id,
                BookingPayment.status == "success",
            )
        )

        return result.scalar() or 0.0


async def get_booking_remain_amount(
    booking_id: int,
):
    async with SessionLocal() as session:

        result = await session.execute(
            select(Booking)
            .where(
                Booking.id == booking_id
            )
        )

        booking = result.scalar_one_or_none()

        if not booking:
            return 0.0

        paid_amount = await get_booking_paid_amount(
            booking_id
        )

        remain_amount = (
            booking.total_price
            - paid_amount
        )

        if remain_amount < 0:
            remain_amount = 0.0

        return remain_amount


async def pay_cash(
    booking_id: int,
    amount: float,
    user_id: int | None = None,
):
    async with SessionLocal() as session:

        result = await session.execute(
            select(Booking)
            .where(
                Booking.id == booking_id
            )
        )

        booking = result.scalar_one_or_none()

        if not booking:
            return None

        payment = BookingPayment(
            booking_id=booking_id,
            amount=amount,
            payment_type="CASH",
            status="success",
        )

        session.add(payment)

        await session.flush()

        paid_result = await session.execute(
            select(
                func.sum(
                    BookingPayment.amount
                )
            ).where(
                BookingPayment.booking_id == booking_id,
                BookingPayment.status == "success",
            )
        )

        paid_amount = (
            paid_result.scalar() or 0.0
        )

        if paid_amount >= booking.total_price:
            booking.status = "confirmed"

        await session.commit()

        await session.refresh(payment)

        return payment


async def pay_card(
    booking_id: int,
    amount: float,
    payment_type: str = "CARD",
    user_id: int | None = None,
):
    async with SessionLocal() as session:

        result = await session.execute(
            select(Booking)
            .where(
                Booking.id == booking_id
            )
        )

        booking = result.scalar_one_or_none()

        if not booking:
            return None

        payment = BookingPayment(
            booking_id=booking_id,
            amount=amount,
            payment_type=payment_type,
            status="success",
        )

        session.add(payment)

        await session.flush()

        paid_result = await session.execute(
            select(
                func.sum(
                    BookingPayment.amount
                )
            ).where(
                BookingPayment.booking_id == booking_id,
                BookingPayment.status == "success",
            )
        )

        paid_amount = (
            paid_result.scalar() or 0.0
        )

        if paid_amount >= booking.total_price:
            booking.status = "confirmed"

        await session.commit()

        await session.refresh(payment)

        return payment
    
async def create_booking(session_id: int, user_id: int, players_count: int, total_price: float):
    async with SessionLocal() as session:
        booking = Booking(
            session_id=session_id,
            user_id=user_id,
            players_count=players_count,
            total_price=total_price,
            status="pending"
        )
        session.add(booking)
        await session.commit()
        await session.refresh(booking)
        return booking


async def get_user_bookings(user_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Booking)
            .options(selectinload(Booking.session).selectinload(Session.game))
            .where(Booking.user_id == user_id)
        )
        return result.scalars().all()


async def add_payment(booking_id: int, amount: float, payment_type: str, transaction_id: str = None):
    async with SessionLocal() as session:
        payment = BookingPayment(
            booking_id=booking_id,
            amount=amount,
            payment_type=payment_type,
            status="success"
        )
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment


# --- Financial & Report Functions ---

async def total_payments():
    async with SessionLocal() as session:
        result = await session.execute(select(func.sum(BookingPayment.amount)))
        return result.scalar() or 0.0


async def today_income(today_date: datetime = None):
    if today_date is None:
        today_date = datetime.utcnow().date()
    async with SessionLocal() as session:
        result = await session.execute(
            select(func.sum(BookingPayment.amount))
            .where(func.date(BookingPayment.created_at) == today_date)
        )
        return result.scalar() or 0.0

# ==========================================================
# SESSION FUNCTIONS
# ==========================================================

async def create_session(
    game_id: int,
    start_time: datetime,
    end_time: datetime,
    capacity: int,
):
    async with SessionLocal() as session:
        new_session = Session(
            game_id=game_id,
            start_time=start_time,
            end_time=end_time,
            capacity=capacity,
            is_active=True,
        )

        session.add(new_session)

        await session.commit()

        await session.refresh(new_session)

        return new_session

    # ==========================================================
# SESSION FUNCTIONS
# ==========================================================

async def get_session(session_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Session)
            .options(
                selectinload(Session.game)
            )
            .where(Session.id == session_id)
        )

        return result.scalar_one_or_none()


async def create_session(
    game_id: int,
    start_time: datetime,
    end_time: datetime,
    capacity: int,
):
    async with SessionLocal() as session:
        new_session = Session(
            game_id=game_id,
            start_time=start_time,
            end_time=end_time,
            capacity=capacity,
            is_active=True,
        )

        session.add(new_session)

        await session.commit()

        await session.refresh(new_session)

        return new_session