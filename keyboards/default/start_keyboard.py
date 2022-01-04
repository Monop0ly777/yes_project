from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    row_width=2,
    keyboard=[
        [
            KeyboardButton(text='🟡 Профіль'),
            KeyboardButton(text='🟡 Магазин'),
        ],
        [
            KeyboardButton(text='🟡 Зворотній зв\'язок')
        ]
    ], resize_keyboard=True
)

start_manager = ReplyKeyboardMarkup(
    row_width=2,
    keyboard=[
        [
            KeyboardButton(text='🟡 Активные заказы'),
        ],
        [
            KeyboardButton(text='🟡 Выполненые заказы'),
        ]
    ], resize_keyboard=True
)

start_admin = ReplyKeyboardMarkup(
    row_width=2,
    keyboard=[
        [
            KeyboardButton(text='🟡 Меню'),
        ],
        [
            KeyboardButton(text='🟡 Активные заказы'),
        ],
        [
            KeyboardButton(text='🟡 Выполненые заказы'),
        ]
    ], resize_keyboard=True
)
