from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hlink

from keyboards.default.start_keyboard import start_admin
from keyboards.inline.admin_keyboard import mailing_for_user_keyboard, admin_mailing, admin_text_keyboard, \
    approve_keyboard, admin_photo_keyboard, admin_video_keyboard, admin_gif_keyboard
from loader import dp, bot
from states.states import Mailing_for_user, Mailing_photo_for_user, Mailing_video_for_user, Mailing_gif_for_user


@dp.callback_query_handler(text='mailing_for_user')
async def mailing_use(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Напишите Telegram ID пользователя', reply_markup=admin_mailing)
    await Mailing_for_user.ID.set()


# Получение контента
@dp.message_handler(state=Mailing_for_user.ID)
async def mailin_id(msg: types.Message, state: FSMContext):
    await state.update_data(user_id=msg.text)
    if msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()
    elif msg.text == 'Далее':
        await msg.answer('Введите Telegram ID')
    else:
        await msg.answer(
            'Отправьте боту то, что хотите опубликовать. Это может быть всё, что угодно – текст, фото, видео',
            reply_markup=admin_mailing)
        await Mailing_for_user.File.set()


# Определение типа контента
@dp.message_handler(state=Mailing_for_user.File, content_types=types.ContentType.ANY)
async def mailin_for_user_content_types(msg: types.Message, state: FSMContext):
    data = await state.get_data('')
    user_id = data.get('user_id')
    if msg.content_type == 'text':
        if msg.text == 'Отменить':
            await msg.answer('Отменено', reply_markup=start_admin)
            await state.finish()
        elif msg.text == 'Далее':
            await msg.answer('Отправьте что то для отправки')
        else:
            await state.update_data(user_id=user_id)
            await state.update_data(text=msg.text)
            await msg.answer(msg.text, reply_markup=admin_text_keyboard, parse_mode='HTML')
            await Mailing_for_user.Buttons.set()
    elif msg.content_type == 'photo':
        if msg.text == 'Отменить':
            await msg.answer('Отменено', reply_markup=start_admin)
            await state.finish()
        elif msg.text == 'Далее':
            await msg.answer('Отправьте что то для отправки')
        else:
            if msg.caption:
                await state.update_data(user_id=user_id)
                await state.update_data(caption=msg.caption)
                await state.update_data(photo=msg.photo[-1].file_id)
                await bot.send_photo(caption=msg.caption, photo=msg.photo[-1].file_id,
                                     reply_markup=admin_photo_keyboard,
                                     parse_mode='HTML', chat_id=msg.chat.id)
                await Mailing_photo_for_user.Buttons.set()
            else:
                await state.update_data(user_id=user_id)
                await state.update_data(photo=msg.photo[-1].file_id)
                await bot.send_photo(photo=msg.photo[-1].file_id, reply_markup=admin_photo_keyboard, parse_mode='HTML',
                                     chat_id=msg.chat.id)
                await Mailing_photo_for_user.Buttons.set()
    elif msg.content_type == 'video':
        if msg.caption:
            await state.update_data(user_id=user_id)
            await state.update_data(caption=msg.caption)
            await state.update_data(video=msg.video.file_id)
            await bot.send_video(caption=msg.caption, video=msg.video.file_id, reply_markup=admin_video_keyboard,
                                 parse_mode='HTML', chat_id=msg.chat.id)
            await Mailing_video_for_user.Buttons.set()
        else:
            await state.update_data(user_id=user_id)
            await state.update_data(video=msg.video.file_id)
            await bot.send_video(video=msg.video.file_id, reply_markup=admin_video_keyboard, parse_mode='HTML',
                                 chat_id=msg.chat.id)
            await Mailing_video_for_user.Buttons.set()
    elif msg.content_type == 'animation':
        if msg.caption:
            await state.update_data(user_id=user_id)
            await state.update_data(caption=msg.caption)
            await state.update_data(gif=msg.animation.file_id)
            await bot.send_animation(caption=msg.caption, animation=msg.animation.file_id, reply_markup=admin_gif_keyboard,
                                 parse_mode='HTML', chat_id=msg.chat.id)
            await Mailing_gif_for_user.Buttons.set()
        else:
            await state.update_data(user_id=user_id)
            await state.update_data(video=msg.animation.file_id)
            await bot.send_animation(animation=msg.animation.file_id, reply_markup=admin_gif_keyboard,
                                     parse_mode='HTML',
                                     chat_id=msg.chat.id)
            await Mailing_gif_for_user.Buttons.set()
    else:
        pass


# ТЕКСТ
@dp.callback_query_handler(text='add_inline_button_text', state=Mailing_for_user.Buttons)
async def mail_for_user_text(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        f'Отправьте мне список URL-кнопок в одном сообщении. Пожалуйста, следуйте этому формату:\n\nКнопка 1 | http://example1.com | Кнопка 2 | http://example2.com')
    await Mailing_for_user.Buttons_info.set()


# ТЕКСТ
# Подтверждение отправки текста без кнопки
@dp.message_handler(state=Mailing_for_user.Buttons)
async def mailin_no_button(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        data = await state.get_data('')
        user_id = data.get('user_id')
        link = hlink('Клик', url=f'tg://user?id={user_id}')
        await msg.answer(f'Вы действительно хотите отправить {link}', reply_markup=approve_keyboard)
        await Mailing_for_user.Approve_without_buttons.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


# ТЕКСТ
# Предпросмотр сообщения с кнопкой
@dp.message_handler(state=Mailing_for_user.Buttons_info)
async def mail_for_user_text_button_info(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()
    else:
        try:
            data = await state.get_data()
            text = data.get('text')
            markup = msg.text
            markup = markup.split(' | ')
            url = []
            text_ = []
            for i in markup:
                if i[0:4] == 'http':
                    url.append(i)
                elif i[0:5] == 'https':
                    url.append(i)
                else:
                    text_.append(i)
            index = 0
            markup = InlineKeyboardMarkup(row_width=1)
            for i in range(0, int(len(text_))):
                markup.insert(
                    InlineKeyboardButton(text=text_[index], url=url[index])
                )
                index += 1
            await msg.answer(text=text, reply_markup=markup, parse_mode='HTML')
            await msg.answer(text='Для действия нажмите нужную вам кнопку')
            await state.update_data(markup=markup)
            await Mailing_for_user.Approve.set()
        except:
            await msg.answer('Вы не правильно написали кнопки')


# ТЕКСТ
# Подверждение отправки, с кнопкой
@dp.message_handler(state=Mailing_for_user.Approve)
async def mail_aprove(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        data = await state.get_data('')
        user_id = data.get('user_id')
        link = hlink('Клик', url=f'tg://user?id={user_id}')
        await msg.answer(text=f'Вы действительно хотите отправить {link}', reply_markup=approve_keyboard)
        await Mailing_for_user.Approve_accept.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено')
        await state.finish()


# ТЕКСТ
# Если подвержденный, рассылка без кнопки
@dp.callback_query_handler(text='accept_mailing', state=Mailing_for_user.Approve_without_buttons)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    user_id = data.get('user_id')
    try:
        await bot.send_message(text=text, chat_id=user_id, parse_mode='HTML')
    except:
        await call.message.answer('Вы указали неверные данные или пользователь остановил бота',
                                  reply_markup=start_admin)
        await state.finish()
    await call.message.answer('Отправлено пользователю')
    await state.finish()


# ТЕКСТ
# Если отмена, с кнопкой
@dp.callback_query_handler(text='cancel_mailing', state=Mailing_for_user.Approve_accept)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


# ТЕКСТ
# Если отмена, без кнопки
@dp.callback_query_handler(text='cancel_mailing', state=Mailing_for_user.Approve_without_buttons)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


# ТЕКСТ
# Если подтвержденный рассылка с кнопкой
@dp.callback_query_handler(text='accept_mailing', state=Mailing_for_user.Approve_accept)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup = data.get('markup')
    text = data.get('text')
    user_id = data.get('user_id')
    try:
        await bot.send_message(text=text, chat_id=user_id, reply_markup=markup, parse_mode='HTML')
    except:
        await call.message.answer('Вы указали неверные данные или пользователь остановил бота',
                                  reply_markup=start_admin)
        await state.finish()
    await call.message.answer('Отправлено пользователю')
    await state.finish()


# ФОТО
@dp.callback_query_handler(text='add_inline_button_photo', state=Mailing_photo_for_user.Buttons)
async def mailin_button(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        f'Отправьте мне список URL-кнопок в одном сообщении. Пожалуйста, следуйте этому формату:\n\nКнопка 1 | http://example1.com | Кнопка 2 | http://example2.com')
    await Mailing_photo_for_user.Buttons_info.set()


# ФОТО
# Подтверждение без кнопки
@dp.message_handler(state=Mailing_photo_for_user.Buttons)
async def mailin_no_button(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        data = await state.get_data('')
        user_id = data.get('user_id')
        link = hlink('Клик', url=f'tg://user?id={user_id}')
        await msg.answer(f'Вы действительно хотите отправить {link}', reply_markup=approve_keyboard)
        await Mailing_photo_for_user.Approve_without_buttons.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено')
        await state.finish()


# ФОТО
# Предпросмотр сообщения с кнопкой
@dp.message_handler(state=Mailing_photo_for_user.Buttons_info)
async def mailin_button_info(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()
    else:
        try:
            data = await state.get_data()
            caption = data.get('caption')
            photo = data.get('photo')
            markup = msg.text
            markup = markup.split(' | ')
            url = []
            text_ = []
            for i in markup:
                if i[0:4] == 'http':
                    url.append(i)
                elif i[0:5] == 'https':
                    url.append(i)
                else:
                    text_.append(i)
            index = 0
            markup = InlineKeyboardMarkup(row_width=1)
            for i in range(0, int(len(text_))):
                markup.insert(
                    InlineKeyboardButton(text=text_[index], url=url[index])
                )
                index += 1
            if caption == None:
                await bot.send_photo(photo=photo, reply_markup=markup, chat_id=msg.chat.id, parse_mode='HTML')
                await msg.answer(text='Для действия нажмите нужную вам кнопку')
                await state.update_data(markup=markup)
                await Mailing_photo_for_user.Approve.set()
            else:
                await bot.send_photo(photo=photo, caption=caption, reply_markup=markup, chat_id=msg.chat.id,
                                     parse_mode='HTML')
                await msg.answer(text='Для действия нажмите нужную вам кнопку')
                await state.update_data(markup=markup)
                await Mailing_photo_for_user.Approve.set()
        except:
            await msg.answer('Вы не правильно написали кнопки')


# ФОТО
# Подверждение с кнопкой
@dp.message_handler(state=Mailing_photo_for_user.Approve)
async def mail_aprove(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        data = await state.get_data('')
        user_id = data.get('user_id')
        link = hlink('Клик', url=f'tg://user?id={user_id}')
        await msg.answer(text=f'Вы действительно хотите отправить {link}', reply_markup=approve_keyboard)
        await Mailing_photo_for_user.Approve_accept.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено')
        await state.finish()


# ФОТО
# Фнкция рассылки с кнопкой
@dp.callback_query_handler(text='accept_mailing', state=Mailing_photo_for_user.Approve_accept)
async def mailing_appo(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup = data.get('markup')
    caption = data.get('caption')
    photo = data.get('photo')
    chat_id = data.get('user_id')
    try:
        if caption == None:
            await bot.send_photo(photo=photo, reply_markup=markup, chat_id=chat_id, parse_mode='HTML')
        else:
            await bot.send_photo(photo=photo, caption=caption, reply_markup=markup, chat_id=chat_id,
                                 parse_mode='HTML')
    except:
        await call.message.answer('Вы указали неверные данные или пользователь остановил бота',
                                  reply_markup=start_admin)
    await call.message.answer('Отправлено пользователю')

    await state.finish()


# ФОТО
# Фнукция рассылки без кнопки
@dp.callback_query_handler(text='accept_mailing', state=Mailing_photo_for_user.Approve_without_buttons)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photo = data.get('photo')
    caption = data.get('caption')
    chat_id = data.get('user_id')

    # Сделать рассылку по пользователям
    try:
        if caption == None:
            await bot.send_photo(chat_id=chat_id, photo=photo, parse_mode='HTML')
        else:
            await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, parse_mode='HTML')
    except:
        await call.message.answer('Вы указали неверные данные или пользователь остановил бота',
                                  reply_markup=start_admin)
    await call.message.answer('Отправлено пользователю')
    await state.finish()


# ФОТО
# Отмена
@dp.callback_query_handler(text='cancel_mailing', state=Mailing_photo_for_user.Approve_accept)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


# ФОТО
# Отмена
@dp.callback_query_handler(text='cancel_mailing', state=Mailing_photo_for_user.Approve_without_buttons)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


# ВИДЕО
@dp.callback_query_handler(text='add_inline_button_video', state=Mailing_video_for_user.Buttons)
async def mailin_button(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.answer(
        f'Отправьте мне список URL-кнопок в одном сообщении. Пожалуйста, следуйте этому формату:\n\nКнопка 1 | http://example1.com | Кнопка 2 | http://example2.com')
    await Mailing_video_for_user.Buttons_info.set()


@dp.message_handler(state=Mailing_video_for_user.Buttons)
async def mailin_no_button(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        data = await state.get_data('')
        user_id = data.get('user_id')
        link = hlink('Клик', url=f'tg://user?id={user_id}')
        await msg.answer(f'Вы действительно хотите отправить {link}', reply_markup=approve_keyboard)
        await Mailing_video_for_user.Approve_without_buttons.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


@dp.message_handler(state=Mailing_video_for_user.Buttons_info)
async def mailin_button_info(msg: types.Message, state: FSMContext):
    if msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()
    else:
        try:
            data = await state.get_data('')
            video = data.get('video')
            caption = data.get('caption')
            markup = msg.text
            markup = markup.split(' | ')
            url = []
            text_ = []
            for i in markup:
                if i[0:4] == 'http':
                    url.append(i)
                elif i[0:5] == 'https':
                    url.append(i)
                else:
                    text_.append(i)
            index = 0
            markup = InlineKeyboardMarkup(row_width=1)
            for i in range(0, int(len(text_))):
                markup.insert(
                    InlineKeyboardButton(text=text_[index], url=url[index])
                )
                index += 1
            if caption == None:
                await bot.send_video(video=video, reply_markup=markup, chat_id=msg.from_user.id, parse_mode='HTML')
            else:
                await bot.send_video(video=video, reply_markup=markup, chat_id=msg.from_user.id, caption=caption,
                                     parse_mode='HTML')
            await msg.answer(text='Для действия нажмите нужную вам кнопку')
            await state.update_data(markup=markup)
            await Mailing_video_for_user.Approve.set()
        except:
            await msg.answer('Вы не правильно написали кнопки')


@dp.callback_query_handler(text='accept_mailing', state=Mailing_video_for_user.Approve_without_buttons)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data('')
    video = data.get('video')
    caption = data.get('caption')
    chat_id = data.get('user_id')
    # Сделать рассылку по пользователям
    try:
        if caption == None:
            await bot.send_video(chat_id=chat_id, video=video, parse_mode='HTML')
        else:
            await bot.send_video(chat_id=chat_id, video=video, caption=caption, parse_mode='HTML')
    except:
        await call.message.answer('Вы указали неверные данные или пользователь остановил бота',
                                  reply_markup=start_admin)
    await call.message.answer('Отправлено пользователю')
    await state.finish()


@dp.message_handler(state=Mailing_video_for_user.Approve)
async def mail_aprove(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        data = await state.get_data('')
        user_id = data.get('user_id')
        link = hlink('Клик', url=f'tg://user?id={user_id}')
        await msg.answer(text=f'Вы действительно хотите отправить {link}', reply_markup=approve_keyboard)
        await Mailing_video_for_user.Approve_accept.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено')
        await state.finish()


@dp.callback_query_handler(text='accept_mailing', state=Mailing_video_for_user.Approve_accept)
async def mailing_appo(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup = data.get('markup')
    caption = data.get('caption')
    video = data.get('video')
    chat_id = data.get('chat_id')
    # Сделать рассылку по пользователям
    try:
        if caption == None:
            await bot.send_video(video=video, reply_markup=markup, chat_id=chat_id, parse_mode='HTML')
        else:
            await bot.send_photo(video=video, caption=caption, reply_markup=markup, chat_id=chat_id,
                                 parse_mode='HTML')
    except:
        await call.message.answer('Вы указали неверные данные или пользователь остановил бота',
                                  reply_markup=start_admin)
    await call.message.answer('Отправлено пользователю')
    await state.finish()

    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing_video_for_user.Approve_accept)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing_video_for_user.Approve_without_buttons)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


# GIF
@dp.callback_query_handler(text='add_inline_button_gif', state=Mailing_gif_for_user.Buttons)
async def mailin_button(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        f'Отправьте мне список URL-кнопок в одном сообщении. Пожалуйста, следуйте этому формату:\n\nКнопка 1 | http://example1.com | Кнопка 2 | http://example2.com')
    await Mailing_gif_for_user.Buttons_info.set()


@dp.message_handler(state=Mailing_gif_for_user.Buttons)
async def mailin_no_button(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        data = await state.get_data('')
        user_id = data.get('user_id')
        link = hlink('Клик', url=f'tg://user?id={user_id}')
        await msg.answer(text=f'Вы действительно хотите отправить {link}', reply_markup=approve_keyboard)
        await Mailing_gif_for_user.Approve_without_buttons.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


@dp.message_handler(state=Mailing_gif_for_user.Buttons_info)
async def mailin_button_info(msg: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        caption = data.get('caption')
        gif = data.get('gif')
        markup = msg.text
        markup = markup.split(' | ')
        url = []
        text_ = []
        for i in markup:
            if i[0:4] == 'http':
                url.append(i)
            elif i[0:5] == 'https':
                url.append(i)
            else:
                text_.append(i)
        index = 0
        markup = InlineKeyboardMarkup(row_width=1)
        for i in range(0, int(len(text_))):
            markup.insert(
                InlineKeyboardButton(text=text_[index], url=url[index])
            )
            index += 1
        if caption == None:
            await bot.send_animation(animation=gif, reply_markup=markup, chat_id=msg.chat.id, parse_mode='HTML')
            await msg.answer(text='Для действия нажмите нужную вам кнопку')
            await state.update_data(markup=markup)
            await Mailing_gif_for_user.Approve.set()
        else:
            await bot.send_animation(animation=gif, caption=caption, reply_markup=markup, chat_id=msg.chat.id,
                                     parse_mode='HTML')
            await msg.answer(text='Для действия нажмите нужную вам кнопку')
            await state.update_data(markup=markup)
            await Mailing_gif_for_user.Approve.set()
    except:
        await msg.answer('Вы не правильно написали кнопки')


@dp.callback_query_handler(text='accept_mailing', state=Mailing_gif_for_user.Approve_without_buttons)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    gif = data.get('gif')
    caption = data.get('caption')
    # Сделать рассылку по пользователям
    user_id = data.get('user_id')
    try:
        if caption == None:
            await bot.send_animation(chat_id=user_id, animation=gif, parse_mode='HTML')
        else:
            await bot.send_animation(chat_id=user_id, animation=gif, caption=caption, parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')
    await state.finish()


@dp.message_handler(state=Mailing_gif_for_user.Approve)
async def mail_aprove(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        data = await state.get_data('')
        user_id = data.get('user_id')
        link = hlink('Клик', url=f'tg://user?id={user_id}')
        await msg.answer(text=f'Вы действительно хотите отправить {link}', reply_markup=approve_keyboard)
        await Mailing_gif_for_user.Approve_accept.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


@dp.callback_query_handler(text='accept_mailing', state=Mailing_gif_for_user.Approve_accept)
async def mailing_appo(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup = data.get('markup')
    caption = data.get('caption')
    gif = data.get('gif')
    # Сделать рассылку по пользователям
    user_id = data.get('user_id')
    try:
        if caption == None:
            await bot.send_animation(animation=gif, reply_markup=markup, chat_id=user_id, parse_mode='HTML')
        else:
            await bot.send_animation(animation=gif, caption=caption, reply_markup=markup, chat_id=user_id,
                                     parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing_gif_for_user.Approve_accept)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing_gif_for_user.Approve_without_buttons)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()
