from aiogram import types
from aiogram.utils.markdown import hlink

from keyboards.inline.purchase_keyboards import purschase_keyboard, show_purchases, change_status, status_change, \
    purschase_keyboard_complete, show_purchases_complete, complete_order_keyboard, delete_complete_order
from loader import dp
from utils.db_api.commands import select_staff_manager, select_staff_admin, get_purchases_id, \
    get_purchases_change_status, purchases_status_successful, get_purchases_complete_id, delete_complete_order_command


# СПИСОК АКТИВНЫХ ЗАКАЗОВ
@dp.message_handler(text='🟡 Активные заказы')
async def purschase(msg: types.Message):
    for i in await select_staff_manager():
        if msg.from_user.id == i.user_id:
            markup = await purschase_keyboard()
            await msg.answer('Список активных заказов', reply_markup=markup)
        else:
            pass
    for a in await select_staff_admin():
        if msg.from_user.id == a.user_id:
            markup = await purschase_keyboard()
            await msg.answer('Список активных заказов', reply_markup=markup)


# СПИСОК ВЫПОЛНЕНЫХ ЗАКАЗОВ
@dp.message_handler(text='🟡 Выполненые заказы')
async def purschase_complete(msg: types.Message):
    for i in await select_staff_manager():
        if msg.from_user.id == i.user_id:
            markup = await purschase_keyboard_complete()
            await msg.answer('Список выполненых заказов', reply_markup=markup)
        else:
            pass
    for a in await select_staff_admin():
        if msg.from_user.id == a.user_id:
            markup = await purschase_keyboard_complete()
            await msg.answer('Список выполненых заказов', reply_markup=markup)


# ИНФОРМАЦИЯ О ЗАКАЗЕ
@dp.callback_query_handler(show_purchases.filter())
async def navigate(call: types.CallbackQuery, callback_data=dict):
    item_id = callback_data.get('item_id')
    order = await get_purchases_id(int(item_id))
    link = hlink('Клик', url=f'tg://user?id={order.user_id}')
    text = f"""
Товар:{order.name}
Количество: {order.quantity}
Статус: {order.status}
Сумма: {order.sum}
Телефон: {order.number}
Логин: @{order.login}
Написать пользователю - {link}
        """
    await call.message.edit_text(text=text, reply_markup=change_status(item_id=item_id))


# ИНФОРМАЦИЯ О ВЫПОЛНЕНОМ ЗАКАЗЕ
@dp.callback_query_handler(show_purchases_complete.filter())
async def navigate(call: types.CallbackQuery, callback_data=dict):
    item_id = callback_data.get('item_id')
    order = await get_purchases_complete_id(int(item_id))
    link = hlink('Клик', url=f'tg://user?id={order.user_id}')
    text = f"""
Товар:{order.name}
Количество: {order.quantity}
Статус: {order.status}
Сумма: {order.sum}
Телефон: {order.number}
Логин:  @{order.login}
Написать пользователю - {link}
        """
    await call.message.edit_text(text=text, reply_markup=complete_order_keyboard(int(item_id)))


# ВЫХОД ИЗ МЕНЮ
@dp.callback_query_handler(text='back_purchase_all_menu:noncomplete')
async def back_purchase(call: types.CallbackQuery):
    markup = await purschase_keyboard()
    await call.message.edit_text(text='Список активных заказов', reply_markup=markup)


# ВЫХОД ИЗ МЕНЮ
@dp.callback_query_handler(text='back_purchase_all_menu:complete')
async def back_purchase(call: types.CallbackQuery):
    markup = await purschase_keyboard_complete()
    await call.message.edit_text(text='Список выполненых заказов', reply_markup=markup)


# ИЗМЕНЕНИЕ СТАТУСА ЗАКАЗА
@dp.callback_query_handler(status_change.filter())
async def change_stat(call: types.CallbackQuery, callback_data=dict):
    item_id = callback_data.get('item_id')
    change_status_name = callback_data.get('status_name')
    order = await get_purchases_id(int(item_id))
    if change_status_name == 'successful':
        await purchases_status_successful(id=int(item_id), name=order.name, quantity=order.quantity, status='Выполнен',
                                          sum=order.sum, number=order.number, login=order.login, user_id=order.user_id)
        await call.answer(text='Статус заказа изменен на "Выполнен"', show_alert=True)
        markup = await purschase_keyboard()
        await call.message.edit_text(text='Список активных заказов', reply_markup=markup)
    elif change_status_name == 'processed':
        await get_purchases_change_status(id=int(item_id), status='Обрабатывается')
        await call.answer(text='Статус изменен на "Обрабатывается"', show_alert=True)


# Удаление выполненого заказа
@dp.callback_query_handler(delete_complete_order.filter())
async def delete_complete(call: types.CallbackQuery, callback_data=dict):
    item_id = callback_data.get('item_id')
    await delete_complete_order_command(int(item_id))
    markup = await purschase_keyboard_complete()
    await call.message.edit_text(text='Список выполненых заказов', reply_markup=markup)
    await call.answer(text='Заказ удален', show_alert=True)

# меню
