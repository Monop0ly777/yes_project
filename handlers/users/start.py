from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.start_keyboard import start_keyboard, start_manager, start_admin
from loader import dp, bot
from utils.db_api import commands
from utils.db_api.commands import select_staff_admin, select_staff_manager, select_staff


# СТАРТ
@dp.message_handler(CommandStart())
async def bot_start(msg: types.Message):
    with open("img/1.jpg", "rb") as file:
        data = file.read()
    user = await commands.select_user(user_id=msg.from_user.id)
    await bot.send_photo(photo=data, caption='Добро пожаловать', reply_markup=start_keyboard, chat_id=msg.from_user.id)
    if not user:
        await commands.add_user(user_id=msg.from_user.id, name=msg.from_user.full_name)


# МЕНЕДЖЕР ПАНЕЛЬ
@dp.message_handler(commands='manager')
async def bot_start_manager(msg: types.Message):
    for m in await select_staff_manager():
        if msg.from_user.id == m.user_id:
            await msg.answer('Держи меню', reply_markup=start_manager)


# АДМИН ПАНЕЛЬ
@dp.message_handler(commands='admin')
async def bot_start_admin(msg: types.Message):
    for i in await select_staff_admin():
        if msg.from_user.id == i.user_id:
            await msg.answer('Держи меню', reply_markup=start_admin)
