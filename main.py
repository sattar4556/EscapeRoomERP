import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database.database import init_db

from handlers.start import router as start_router
from handlers.menu import router as menu_router
from handlers.games import router as games_router
from handlers.admin import router as admin_router
from handlers.session import router as session_router
from handlers.booking import router as booking_router
from handlers.payment import router as payment_router

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(menu_router)
dp.include_router(games_router)
dp.include_router(admin_router)
dp.include_router(session_router)


async def main():
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
async def main():
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())