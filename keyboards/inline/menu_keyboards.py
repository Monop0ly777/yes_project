from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.db_api.commands import get_categories, get_subcategories, get_items

menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
buy_item = CallbackData("buy", "item_id")


def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(level=level, category=category, subcategory=subcategory, item_id=item_id)


async def categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await get_categories()
    for category in categories:
        btn_text = f"{category.category_name}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category.category_code)

        markup.insert(
            InlineKeyboardButton(text=btn_text, callback_data=callback_data)
        )
    return markup


async def subcategories_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    subcategories = await get_subcategories(category)
    for subcategory in subcategories:
        btn_text = f"{subcategory.subcategory_name}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category,
                                           subcategory=subcategory.subcategory_code)
        markup.insert(
            InlineKeyboardButton(text=btn_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )
    return markup


async def items_keyboard(category, subcategory):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    items = await get_items(category, subcategory)

    for item in items:
        btn_text = f"{item.name} - {item.price} YS"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category, subcategory=subcategory,
                                           item_id=str(item.id))
        markup.insert(
            InlineKeyboardButton(text=btn_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category))
    )
    return markup


def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Купити', callback_data=buy_item.new(item_id=item_id))
    )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category, subcategory=subcategory))
    )
    return markup
