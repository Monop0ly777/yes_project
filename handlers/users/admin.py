from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

from keyboards.default.start_keyboard import start_admin
from keyboards.inline.admin_keyboard import admin_menu_keyboard, admin_back_to_menu, admin_cancel, staff_add_keyboard
from loader import dp, bot
from states.states import Change_user_balance, Add_user_balance, Send_coins_for_user, add_staff_
from utils.db_api.admin_commands import get_all_orders, get_all_orders_promocodes, user_balance_update, \
    user_balance_add, get_all_orders_complete, user_balance_add_invd, staff_add_db
from utils.db_api.commands import select_staff_admin, select_all_users


@dp.message_handler(text='🟡 Меню')
async def admin_menu_handler(msg: types.Message):
    for a in await select_staff_admin():
        if msg.from_user.id == a.user_id:
            await msg.answer('Выберите действие:', reply_markup=admin_menu_keyboard)


@dp.callback_query_handler(text='admin_menu')
async def admin_menu_handler(call: CallbackQuery):
    await call.message.edit_text('Выберите действие:', reply_markup=admin_menu_keyboard)


@dp.callback_query_handler(text='stat_user')
async def admin_stat_user(call: CallbackQuery):
    users_count = len(await select_all_users())
    orders_count = len(await get_all_orders())
    orders_promocodes_count = len(await get_all_orders_promocodes())
    orders_complete_count = len(await get_all_orders_complete())
    await call.message.edit_text(
        f'Статистика \n\nВсего пользователей: {users_count}\nВсего активных заказов: {orders_count}\nВсего выполненых заказов: {orders_complete_count}\nВсего покупок промокодов: {orders_promocodes_count}',
        reply_markup=admin_back_to_menu)


@dp.callback_query_handler(text='change_user_balance')
async def admin_setting_change_user_balance(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите Telegram ID пользователя: ', reply_markup=admin_cancel)
    await Change_user_balance.ID.set()


@dp.message_handler(state=Change_user_balance.ID)
async def admin_setting_change_user_balance_amount(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await state.finish()
        await msg.answer('Выберите действие:', reply_markup=start_admin)
    else:
        await msg.answer('Введите число: ', reply_markup=admin_cancel)
        await Change_user_balance.Amount.set()


@dp.message_handler(state=Change_user_balance.Amount)
async def admin_setting_change_user_balance_(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await state.finish()
        await msg.answer('Выберите действие:', reply_markup=start_admin)
    else:
        await user_balance_update(id=msg.from_user.id, amount=int(msg.text))
        await state.finish()
        await msg.answer('Баланс пользователя изменен')
        await msg.answer('Выберите действие:', reply_markup=start_admin)
        await state.finish()


@dp.callback_query_handler(text='send_yes_coin')
async def admin_send_yes_coins(call: CallbackQuery):
    await call.message.answer('Введите число:', reply_markup=admin_cancel)
    await Add_user_balance.Amount.set()


@dp.message_handler(state=Add_user_balance.Amount)
async def admin_send_coins_amount(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await state.finish()
        await msg.answer('Выберите действие:', reply_markup=start_admin)
    else:
        await user_balance_add(amount=int(msg.text))
        users = await select_all_users()
        for i in users:
            await bot.send_message(chat_id=i.user_id, text=f'🎁 На ваш баланс добавлено + {msg.text} Yes Coin',
                                   reply_markup=start_admin)
        await msg.answer('Операция выполнена успешно')
        await msg.answer('Выберите действие:', reply_markup=start_admin)
        await state.finish()


@dp.callback_query_handler(text='send_yes_coin_indv')
async def send_coin_invd(call: CallbackQuery):
    await call.message.answer('Отправьте Telegram ID пользователя', reply_markup=admin_cancel)
    await Send_coins_for_user.q1.set()


@dp.message_handler(state=Send_coins_for_user.q1)
async def send_coin_invd(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()
    else:
        await state.update_data(user_id=msg.text)
        await msg.answer('Напишите количество монеты', reply_markup=admin_cancel)
        await Send_coins_for_user.q2.set()


@dp.message_handler(state=Send_coins_for_user.q2)
async def send_coin_oinvs(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()
    else:
        try:
            data = await state.get_data()
            id = data.get('user_id')
            await user_balance_add_invd(amount=int(msg.text), id=int(id))
            await bot.send_message(chat_id=id, text=f'🎁 На ваш баланс добавлено + {msg.text} Yes Coin',
                                   reply_markup=start_admin)
            await msg.answer('Монеты отправлены пользователю')
            await state.finish()
        except:
            await msg.answer('Произошла ошибка')


@dp.callback_query_handler(text='staff_add')
async def add_staff(call: CallbackQuery):
    await call.message.answer('Напишите Telegram ID пользователя', reply_markup=admin_cancel)
    await add_staff_.q1.set()


@dp.message_handler(state=add_staff_.q1)
async def add_staff_id(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()
    else:
        await state.update_data(user_id=msg.text)
        await msg.answer('Задайте имя для пользователя', reply_markup=admin_cancel)
        await add_staff_.q2.set()


@dp.message_handler(state=add_staff_.q2)
async def add_ngdfkg(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()
    else:
        await state.update_data(name=msg.text)
        await msg.answer('Задайте должность', reply_markup=staff_add_keyboard)
        await add_staff_.q3.set()


@dp.message_handler(state=add_staff_.q3)
async def add_staff_dolzh(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()
    else:
        try:
            if msg.text == 'Админ':
                data = await state.get_data('')
                user_id = data.get('user_id')
                name = data.get('name')
                await staff_add_db(user_id=int(user_id), name=name, position=msg.text)
                link = hlink(title=data.get('name'), url=f"tg://user?id={data.get('user_id')}")
                await msg.answer(f'Должность - Админ\nНазначен пользователь {link}')
                await state.finish()
            elif msg.text == 'Менеджер':
                data = await state.get_data('')
                user_id = data.get('user_id')
                name = data.get('name')
                await staff_add_db(user_id=int(user_id), name=name, position=msg.text)
                link = hlink(title=data.get('name'), url=f"tg://user?id={data.get('user_id')}")
                await msg.answer(f'Должность - Менеджер\nНазначен пользователь {link}')
                await state.finish()
        except:
            await msg.answer('Произошла ошибка')
