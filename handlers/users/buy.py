from typing import Union
from webbrowser import get

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_keyboard
from keyboards.default.buy_keyboards import phone, cancel, confirmed
from keyboards.inline.menu_keyboards import buy_item
from loader import dp, bot
from states.states import Items, Promocodes
from utils.db_api.commands import get_item, select_user, spend_balance, select_staff_manager, select_staff_admin, \
    add_purchase, select_staff, get_promocode, add_purchase_confirmed, add_purchase_promocodes, get_promocodes_count, \
    promocodes_successful


@dp.callback_query_handler(buy_item.filter())
async def buy(call: types.CallbackQuery, state: FSMContext, callback_data=dict):
    item_id = callback_data.get('item_id')
    item = await get_item(item_id=int(item_id))
    await state.update_data(item_id=item_id)
    promocodes_count = len(await get_promocodes_count(item.promocode_index))
    if item.promocode_index:
        await call.message.answer(f'В наявності: {promocodes_count}', reply_markup=cancel)
        await Promocodes.quantity.set()
    else:
        await call.message.answer('Введіть кількість:', reply_markup=cancel)
        await Items.quantity.set()


@dp.message_handler(state=Items.quantity)
async def tele_number(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    user = await select_user(msg.from_user.id)
    item_id = data.get('item_id')
    item = await get_item(int(item_id))
    await state.update_data(quantity=msg.text)
    if msg.text == 'Скасувати':
        await state.finish()
        await msg.answer('Скасовано', reply_markup=start_keyboard.start_keyboard)
    elif msg.text == '0':
        await msg.answer('Кількість не може дорівнювати нулю')
    if int(user.yes_coin_balance) < int(msg.text) * int(item.price):
        await msg.answer('Ваш баланс менший')
    elif int(user.yes_coin_balance) >= int(msg.text) * int(item.price):
        await msg.answer('Введіть номер телефону або натисніть на кнопку нижче ⬇', reply_markup=phone)
        await Items.number.set()
    else:
        pass


@dp.message_handler(state=Promocodes.quantity)
async def tele_number(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    user = await select_user(msg.from_user.id)
    item_id = data.get('item_id')
    item = await get_item(int(item_id))
    await state.update_data(quantity=msg.text)
    if msg.text == 'Скасувати':
        await state.finish()
        await msg.answer('Скасовано', reply_markup=start_keyboard.start_keyboard)
    elif msg.text == '0':
        await msg.answer('Кількість не може дорівнювати нулю')
    elif int(user.yes_coin_balance) < int(msg.text) * int(item.price):
        await msg.answer('Ваш баланс менший')
    elif int(len(await get_promocodes_count(item.promocode_index))) >= int(msg.text):
        await msg.answer(
            f'З вашого балансу спишеться {int(item.price) * int(msg.text)}\nНатисніть "Підтвердити" для покупки ⬇',
            reply_markup=confirmed)
        await Promocodes.confirm.set()
    else:
        await msg.answer('Кількість більше наявності')


@dp.message_handler(state=Items.number, content_types=types.ContentType.CONTACT)  #
async def tele_number(msg: types.Message, state: FSMContext):
    contact = msg.contact.phone_number
    await state.update_data(phone=contact)
    data = await state.get_data()
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    item = await get_item(int(item_id))
    await msg.answer(f"""
Ваше замовлення:
Назва: {item.name}
Кількість: {quantity}
Сума замовлення: {int(item.price) * int(quantity)} YS

Ваші дані:
{msg.from_user.full_name}
@{msg.from_user.username}
{contact}

Якщо все правильно, натисніть "Підтвердити ⬇"
""", reply_markup=confirmed)
    await Items.confirm.set()


@dp.message_handler(state=Items.number, content_types=types.ContentType.TEXT)
async def tele_number_text(msg: types.Message, state: FSMContext):
    if msg.text == 'Скасувати':
        await msg.answer('Скасовано', reply_markup=start_keyboard.start_keyboard)
        await state.finish()
    else:
        try:
            contact = msg.text
            await state.update_data(phone=contact)
            data = await state.get_data()
            item_id = data.get('item_id')
            quantity = data.get('quantity')
            item = await get_item(int(item_id))
            await msg.answer(f"""        
Ваше замовлення:
Назва: {item.name}
Кількість: {quantity}
Сума замовлення: {int(item.price) * int(quantity)} YS

Ваші дані:
{msg.from_user.full_name}
@{msg.from_user.username}
{contact}

Якщо все правильно, натисніть "Підтвердити ⬇"
    """, reply_markup=confirmed)
        except:
            pass
        await Items.confirm.set()


@dp.message_handler(state=Items.confirm)
async def tele_number_text(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    item = await get_item(int(item_id))
    amount = int(item.price) * int(quantity)
    phone = data.get('phone')
    if msg.text == 'Підтвердити':
        stuff = await select_staff()
        await spend_balance(user_id=msg.from_user.id, amount=amount)
        await add_purchase(user_id=msg.from_user.id, quantity=int(quantity),
                           name=item.subcategory_name + ' ' + item.name,
                           login=msg.from_user.username, number=phone, sum=amount, status='Новый')
        try:
            for stuffs in stuff:
                await bot.send_message(chat_id=stuffs.user_id, text='У вас новый заказа')
        except:
            pass
        await msg.answer("🟡 Ми отримали ваше замовлення, з вами зв'яжеться наш менеджер",
                         reply_markup=start_keyboard.start_keyboard)
        await state.finish()
    elif msg.text == 'Скасувати':
        await msg.answer('Скасувано', reply_markup=start_keyboard.start_keyboard)
        await state.finish()


@dp.message_handler(state=Promocodes.confirm)
async def buy_promocode(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    item = await get_item(int(item_id))
    amount = int(item.price) * int(quantity)
    if msg.text == 'Подтвердить':
        await spend_balance(user_id=msg.from_user.id, amount=amount)

        await msg.answer(text='Ваші промокоди:⬇',
                         reply_markup=start_keyboard.start_keyboard)
        # for i in range(0,int(quantity)):
        #     promocodes = await get_promocode(index=item.promocode_index)
        #     await msg.answer(promocodes.data)
        promocodes = await get_promocode(index=item.promocode_index, quantity=quantity)
        for i in promocodes:
            await msg.answer(text=i.data)
            await add_purchase_promocodes(user_id=msg.from_user.id, quantity=int(quantity),
                                          name=item.subcategory_name + ' ' + item.name,
                                          login=msg.from_user.username, sum=amount, data=i.data)
        await state.finish()
    elif msg.text == 'Скасувати':
        await msg.answer('Скасувано', reply_markup=start_keyboard.start_keyboard)
        await state.finish()
