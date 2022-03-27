from aiogram import executor
from handlers import dp
import filters


async def on_startup(dp):
    filters.setup(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
