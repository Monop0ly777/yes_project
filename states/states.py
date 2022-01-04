from aiogram.dispatcher.filters.state import StatesGroup, State


class Items(StatesGroup):
    quantity = State()
    number = State()
    confirm = State()


class Promocodes(StatesGroup):
    quantity = State()
    confirm = State()


class Change_user_balance(StatesGroup):
    ID = State()
    Amount = State()


class Add_user_balance(StatesGroup):
    Amount = State()


class Mailing(StatesGroup):
    ID = State()
    File = State()
    Buttons = State()
    Buttons_info = State()
    Without_buttons = State()
    Approve = State()
    Approve_without_buttons = State()
    Approve_accept = State()
    Approve_accept_without_buttons = State()


class Mailing_photo(StatesGroup):
    ID = State()
    File = State()
    Buttons = State()
    Buttons_info = State()
    Without_buttons = State()
    Approve = State()
    Approve_without_buttons = State()
    Approve_accept = State()
    Approve_accept_without_buttons = State()


class Mailing_video(StatesGroup):
    ID = State()
    File = State()
    Buttons = State()
    Buttons_info = State()
    Without_buttons = State()
    Approve = State()
    Approve_without_buttons = State()
    Approve_accept = State()
    Approve_accept_without_buttons = State()


class Mailing_gif(StatesGroup):
    ID = State()
    File = State()
    Buttons = State()
    Buttons_info = State()
    Without_buttons = State()
    Approve = State()
    Approve_without_buttons = State()
    Approve_accept = State()
    Approve_accept_without_buttons = State()


class Mailing_for_user(StatesGroup):
    ID = State()
    File = State()
    Buttons = State()
    Buttons_info = State()
    Without_buttons = State()
    Approve = State()
    Approve_without_buttons = State()
    Approve_accept = State()
    Approve_accept_without_buttons = State()


class Mailing_photo_for_user(StatesGroup):
    ID = State()
    File = State()
    Buttons = State()
    Buttons_info = State()
    Without_buttons = State()
    Approve = State()
    Approve_without_buttons = State()
    Approve_accept = State()
    Approve_accept_without_buttons = State()


class Mailing_video_for_user(StatesGroup):
    ID = State()
    File = State()
    Buttons = State()
    Buttons_info = State()
    Without_buttons = State()
    Approve = State()
    Approve_without_buttons = State()
    Approve_accept = State()
    Approve_accept_without_buttons = State()


class Mailing_gif_for_user(StatesGroup):
    ID = State()
    File = State()
    Buttons = State()
    Buttons_info = State()
    Without_buttons = State()
    Approve = State()
    Approve_without_buttons = State()
    Approve_accept = State()
    Approve_accept_without_buttons = State()


class Feedback(StatesGroup):
    q1 = State()
    q2 = State()


class Send_coins_for_user(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()

class add_staff_(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
