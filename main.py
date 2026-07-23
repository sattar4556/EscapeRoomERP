import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database.database import init_db
from handlers.start import router

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def main():
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())