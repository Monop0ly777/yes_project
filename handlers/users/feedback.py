from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

from keyboards.default.start_keyboard import start_keyboard
from keyboards.inline.purchase_keyboards import feedback_accept, feedback_keyboard
from loader import dp, bot
from states.states import Feedback
from utils.db_api.commands import select_staff_admin


@dp.message_handler(text='🟡 Зворотній зв\'язок')
async def feedback(message: types.Message):
    await message.answer('💬 Напишіть ваші побажання та ідеї, щоб покращити цей проект', reply_markup=feedback_keyboard)
    await Feedback.q1.set()


@dp.message_handler(state=Feedback.q1)
async def aprrove_feedback(msg: types.Message, state: FSMContext):
    if msg.text == 'Скасувати':
        await msg.answer('Скасувано', reply_markup=start_keyboard)
        await state.finish()
    else:
        await msg.answer('Відправити?', reply_markup=feedback_accept)
        await Feedback.q2.set()
    await state.update_data(text=msg.text)
    await state.update_data(user_id=msg.from_user.id)
    await state.update_data(fullname=msg.from_user.full_name)



@dp.callback_query_handler(text='accept_feedback', state=Feedback.q2)
async def mailing_feedback(call: CallbackQuery, state: FSMContext):
    data = await state.get_data('')
    text = data.get('text')
    user_id = data.get('user_id')
    fullname = data.get('fullname')
    user = hlink(title=fullname, url=f'tg://user?id={user_id}')
    text = f'{text}\n\nОтправлено от {user}'
    for i in await select_staff_admin():
        await bot.send_message(text=text, chat_id=i.user_id)
    await call.message.answer('Відправлено')
    await state.finish()


@dp.callback_query_handler(text='cancel_feedback', state=Feedback.q2)
async def mailing_feedback(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Скасовано', reply_markup=start_keyboard)
    await state.finish()
