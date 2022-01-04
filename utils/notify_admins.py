import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admins in ADMINS:
        try:
            await dp.bot.send_message(chat_id=admins, text="Бот Запущен")

        except Exception as err:
            logging.exception(err)
