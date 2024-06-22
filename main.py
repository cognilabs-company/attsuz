import logging
import sys
import asyncio

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from config import *
# from functions.teacher import router as teacher_router
from functions.registration import router as registration_router


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    dp.include_router(registration_router)
    # dp.include_router(teacher_router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())