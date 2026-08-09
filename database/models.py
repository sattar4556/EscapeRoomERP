from datetime import datetime
from sqlalchemy import (
    String,
    Boolean,
    ForeignKey,
    BigInteger,
    Integer,
    DateTime,
    Float,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    branches: Mapped[list["Branch"]] = relationship("Branch", back_populates="organization")
    users: Mapped[list["User"]] = relationship("User", back_populates="organization")
    games: Mapped[list["Game"]] = relationship("Game", back_populates="organization")


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str] = mapped_column(String(150))
    city: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(300))
    phone: Mapped[str] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="branches")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), default=1)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    login_count: Mapped[int] = mapped_column(Integer, default=0)
    last_login: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="users")
    roles: Mapped[list["Role"]] = relationship("Role", secondary="user_roles", back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)

    users: Mapped[list["User"]] = relationship("User", secondary="user_roles", back_populates="roles")


class UserRole(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), default=1)
    title: Mapped[str] = mapped_column(String(150))
    genre: Mapped[str] = mapped_column(String(100))
    duration: Mapped[int] = mapped_column(Integer)
    min_players: Mapped[int] = mapped_column(Integer)
    max_players: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float, default=0.0)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="games")
    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="game")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    capacity: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    game: Mapped["Game"] = relationship("Game", back_populates="sessions")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="session")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    players_count: Mapped[int] = mapped_column(Integer)
    total_price: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    session: Mapped["Session"] = relationship("Session", back_populates="bookings")
    user: Mapped["User"] = relationship("User")
    payments: Mapped[list["BookingPayment"]] = relationship("BookingPayment", back_populates="booking")


class BookingPayment(Base):
    __tablename__ = "booking_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    amount: Mapped[float] = mapped_column(Float)
    payment_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default="success")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    booking: Mapped["Booking"] = relationship("Booking", back_populates="payments")