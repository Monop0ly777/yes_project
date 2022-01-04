from typing import Union

from aiogram import types

from keyboards.inline.menu_keyboards import categories_keyboard, subcategories_keyboard, items_keyboard, item_keyboard, \
    menu_cd
from loader import dp, bot
from utils.db_api.commands import get_item


@dp.message_handler(text='🟡 Магазин')
async def show_menu(msg: types.Message):
    await list_categories(msg)


async def list_categories(msg: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()
    if isinstance(msg, types.Message):
        with open("img/3.jpg", "rb") as file:
            data = file.read()
        # await msg.answer('Смотри что у нас есть', reply_markup=markup)
        await bot.send_photo(photo=data,caption='Дивись, що у нас є 😉',chat_id=msg.from_user.id, reply_markup=markup )
    elif isinstance(msg, types.CallbackQuery):
        call = msg
        await call.message.edit_reply_markup(markup)


async def list_subcategories(call: types.CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    await call.message.edit_reply_markup(markup)


async def list_items(call: types.CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category=category, subcategory=subcategory)
    await call.message.edit_caption("Дивись, що у нас є 😉", reply_markup=markup)


async def show_item(call: types.CallbackQuery, category, subcategory, item_id):
    markup = item_keyboard(category, subcategory, item_id)
    item = await get_item(item_id)
    text = item
    await call.message.edit_caption(text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data=dict):
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    item_id = int(callback_data.get('item_id'))
    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_items,
        "3": show_item,
    }
    current_level_function = levels[current_level]
    await current_level_function(
        call,
        category=category,
        subcategory=subcategory,
        item_id=int(item_id),
    )
