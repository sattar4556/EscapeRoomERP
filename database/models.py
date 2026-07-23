from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    ForeignKey,
    BigInteger,
    Integer,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(150))

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id")
    )

    name: Mapped[str] = mapped_column(
        String(150)
    )

    city: Mapped[str] = mapped_column(
        String(100)
    )

    address: Mapped[str] = mapped_column(
        String(300)
    )

    phone: Mapped[str] = mapped_column(
        String(20)
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id")
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True
    )

    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    first_name: Mapped[str] = mapped_column(
        String(100)
    )

    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    is_banned: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    login_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    last_login: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True
    )


class UserRole(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id")
    )


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id")
    )

    title: Mapped[str] = mapped_column(
        String(150)
    )

    genre: Mapped[str] = mapped_column(
        String(100)
    )

    duration: Mapped[int]

    min_players: Mapped[int]

    max_players: Mapped[int]

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )