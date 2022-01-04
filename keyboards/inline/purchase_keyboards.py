from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.db_api.commands import get_items, get_purchases, get_purchases_complete

show_purchases = CallbackData("order", "item_id")
show_purchases_complete = CallbackData("order_complete", "item_id")
status_change = CallbackData("status", "status_name", "item_id")
delete_complete_order = CallbackData("delete_complete_order", "item_id")


async def purschase_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await get_purchases()
    for category in categories:
        btn_text = f"{category.status}"
        markup.insert(
            InlineKeyboardButton(text=btn_text, callback_data=show_purchases.new(item_id=category.id))
        )
    return markup


async def purschase_keyboard_complete():
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await get_purchases_complete()
    for category in categories:
        btn_text = f"{category.name}"
        markup.insert(
            InlineKeyboardButton(text=btn_text, callback_data=show_purchases_complete.new(item_id=category.id))
        )
    return markup


def change_status(item_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Выполнен',
                                     callback_data=status_change.new(status_name='successful', item_id=item_id)),
                InlineKeyboardButton(text='Обрабатывается',
                                     callback_data=status_change.new(status_name='processed', item_id=item_id))

            ],
            [
                InlineKeyboardButton(text='Вернутся назад', callback_data='back_purchase_all_menu:noncomplete')
            ]
        ]
    )
    return markup


def complete_order_keyboard(item_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Удалить',
                                     callback_data=delete_complete_order.new(item_id=item_id)),
            ],
            [
                InlineKeyboardButton(text='Вернутся назад', callback_data='back_purchase_all_menu:complete')
            ]
        ]
    )
    return markup


feedback_accept = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Скасувати', callback_data='cancel_feedback'),
            InlineKeyboardButton(text='Відправити', callback_data='accept_feedback'),
        ]
    ]
)

feedback_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Скасувати'),
        ]
    ], resize_keyboard=True
)
