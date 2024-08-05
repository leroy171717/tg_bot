import asyncio
from aiogram import Bot, Dispatcher

from handlers import router
from database.models import async_main

async def main():
    await async_main()
    bot = Bot(token='6801002660:AAFnGvUQ6VYbWLZ0v1JPkmw3a2uoWylKtZQ')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
