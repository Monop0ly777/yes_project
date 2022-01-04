from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

admin_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассылка', callback_data='mailing')

        ],        [
            InlineKeyboardButton(text='Рассылка инд.', callback_data='mailing_for_user')

        ],
        [
            InlineKeyboardButton(text='Статистика', callback_data='stat_user'),
        ],
        [
            InlineKeyboardButton(text='Изменить баланс пользователю', callback_data='change_user_balance')
        ],
        [
            InlineKeyboardButton(text='Отправить всем пользователям Yes Coin', callback_data='send_yes_coin')
        ],
        [
            InlineKeyboardButton(text='Отправить пользователю Yes Coin', callback_data='send_yes_coin_indv')
        ],
        [
            InlineKeyboardButton(text='Добавить персонал', callback_data='staff_add')
        ],
    ]
)
admin_back_to_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Вернутся назад', callback_data='admin_menu')
        ]
    ]
)

admin_cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отменить')
        ],
    ], resize_keyboard=True
)
admin_mailing = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Далее')
        ],
        [
            KeyboardButton(text='Отменить')
        ],

    ], resize_keyboard=True
)

admin_text_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить кнопки', callback_data='add_inline_button_text')
        ]
    ]
)

admin_photo_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить кнопки', callback_data='add_inline_button_photo')
        ]
    ]
)

admin_gif_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить кнопки', callback_data='add_inline_button_gif')
        ]
    ]
)
admin_video_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить кнопки', callback_data='add_inline_button_video')
        ]
    ]
)

approve_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отменить', callback_data='cancel_mailing'),
            InlineKeyboardButton(text='Отправить', callback_data='accept_mailing'),
        ]
    ]
)
mailing_for_user_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отменить', callback_data='cancel_mailing'),
            InlineKeyboardButton(text='Отправить', callback_data='accept_mailing'),
        ]
    ]
)

staff_add_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Админ'),
            KeyboardButton(text='Менеджер')
        ],
        [
            KeyboardButton(text='Отменить')
        ]
    ], resize_keyboard=True
)