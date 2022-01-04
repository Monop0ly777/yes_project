import asyncio

from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.db_api.db_gino import create_db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api import db_gino


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды

    await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    await db_gino.on_startup(dp)
    await create_db()
    # await asyncio.sleep(5)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
