from datetime import datetime

from sqlalchemy import select

from database.database import SessionLocal
from database.models import User


async def get_user(telegram_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
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

            await session.commit()

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