from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Надіслати номер телефону", request_contact=True),
        ],
        [
            KeyboardButton(text="Скасувати")
        ]
    ], resize_keyboard=True
)
cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Скасувати")
        ]
    ], resize_keyboard=True
)

confirmed = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Підтвердити')
        ],
        [
            KeyboardButton(text='Скасувати')
        ]
    ], resize_keyboard=True
)
