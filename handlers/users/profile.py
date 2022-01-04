from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode

from loader import dp, bot
from utils.db_api import commands


@dp.message_handler(text='🟡 Профіль')
async def profile(msg: types.Message):
    with open('img/4.jpg', 'rb') as file:
        data = file.read()
    user_id = hcode(msg.chat.id)
    user = await commands.select_user(user_id=msg.from_user.id)
    await bot.send_photo(photo=data, chat_id=msg.chat.id, caption=f"""
<b>👥 Твої дані:</b> <i>{msg.from_user.full_name}</i>

<b>🆔 Твій ID:</b> <i>{user_id}</i>
<b>💰 Кількість YesCoin:</b><i> {user.yes_coin_balance}</i>
""", parse_mode='HTML')


@dp.callback_query_handler(text='profile')
async def profile(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    with open('img/4.jpg', 'rb') as file:
        data = file.read()
    user_id = hcode(call.message.chat.id)
    user = await commands.select_user(user_id=call.from_user.id)
    await bot.send_photo(photo=data, chat_id=call.message.chat.id, caption=f"""
<b>👥 Твої дані:</b> <i></i>
<b>🆔 Твій ID:</b> <i>{user_id}</i>

<b>💰 Кількість YesCoin:</b> {user.yes_coin_balance} <i></i>
""", parse_mode='HTML')
