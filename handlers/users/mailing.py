from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.default.start_keyboard import start_admin
from keyboards.inline.admin_keyboard import admin_mailing, admin_photo_keyboard, admin_text_keyboard, \
    admin_gif_keyboard, admin_video_keyboard, approve_keyboard
from loader import dp, bot
from states.states import Mailing, Mailing_photo, Mailing_video, Mailing_gif
from utils.db_api.commands import select_all_users


@dp.callback_query_handler(text='mailing')
async def admin_mailin(call: CallbackQuery):
    await call.message.answer(
        'Отправьте боту то, что хотите опубликовать. Это может быть всё, что угодно – текст, фото, видео',
        reply_markup=admin_mailing)

    await Mailing.File.set()


@dp.message_handler(state=Mailing.File, content_types=types.ContentType.ANY)
async def admin_mailin_2(msg: types.Message, state: FSMContext):
    if msg.content_type == 'text':
        if msg.text == 'Отменить':
            await msg.answer('Отменено', reply_markup=start_admin)
            await state.finish()
        elif msg.text == 'Далее':
            await msg.answer('Отправьте какой-то контент')
        else:
            await state.update_data(text=msg.text)
            await msg.answer(text=msg.text, reply_markup=admin_text_keyboard, parse_mode='HTML')
            await Mailing.Buttons.set()
    elif msg.content_type == 'photo':
        await state.update_data(photo=msg.photo[-1].file_id)
        if msg.caption == None:
            await bot.send_photo(photo=msg.photo[-1].file_id, reply_markup=admin_photo_keyboard, chat_id=msg.chat.id,
                                 parse_mode='HTML')
            await Mailing_photo.Buttons.set()
        else:
            await bot.send_photo(photo=msg.photo[-1].file_id, caption=msg.caption, reply_markup=admin_photo_keyboard,
                                 chat_id=msg.chat.id, parse_mode='HTML')
            await state.update_data(caption=msg.caption)
            await Mailing_photo.Buttons.set()
    elif msg.content_type == 'animation':
        await state.update_data(caption=msg.caption)
        await state.update_data(gif=msg.animation.file_id)
        if msg.caption == None:
            await bot.send_animation(animation=msg.animation.file_id, reply_markup=admin_gif_keyboard,
                                     chat_id=msg.chat.id, parse_mode='HTML')
            await Mailing_gif.Buttons.set()
        else:
            await bot.send_animation(animation=msg.animation.file_id, reply_markup=admin_gif_keyboard,
                                     caption=msg.caption, chat_id=msg.from_user.id, parse_mode='HTML')
            await Mailing_gif.Buttons.set()

    elif msg.content_type == 'video':
        await state.update_data(video=msg.video.file_id)
        await state.update_data(caption=msg.caption)
        if msg.caption == None:
            await bot.send_video(video=msg.video.file_id, reply_markup=admin_video_keyboard, chat_id=msg.chat.id,
                                 parse_mode='HTML')
            await Mailing_video.Buttons.set()
        else:
            await bot.send_video(video=msg.video.file_id, reply_markup=admin_video_keyboard, caption=msg.caption,
                                 chat_id=msg.chat.id, parse_mode='HTML')
            await Mailing_video.Buttons.set()
    else:
        pass


@dp.callback_query_handler(text='add_inline_button_text', state=Mailing.Buttons)
async def mailin_button(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        f'Отправьте мне список URL-кнопок в одном сообщении. Пожалуйста, следуйте этому формату:\n\nКнопка 1 | http://example1.com | Кнопка 2 | http://example2.com')
    await Mailing.Buttons_info.set()


@dp.message_handler(state=Mailing.Buttons)
async def mailin_no_button(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        await msg.answer('Вы действительно хотите отправить', reply_markup=approve_keyboard)
        await Mailing.Approve_without_buttons.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


@dp.message_handler(state=Mailing.Buttons_info)
async def mailin_button_info(msg: types.Message, state: FSMContext):
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
            await Mailing.Approve.set()
        except:
            await msg.answer('Вы не правильно написали кнопки')


@dp.message_handler(state=Mailing.Approve)
async def mail_aprove(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        await msg.answer(text='Вы действительно хотите отправить', reply_markup=approve_keyboard)
        await Mailing.Approve_accept.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


# Рассылка без кнопки
@dp.callback_query_handler(text='accept_mailing', state=Mailing.Approve_without_buttons)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    users = await select_all_users()
    try:
        for i in users:
            await bot.send_message(text=text, chat_id=i.user_id, parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing.Approve_accept)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing.Approve_without_buttons)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


# Рассылка с кнопкой
@dp.callback_query_handler(text='accept_mailing', state=Mailing.Approve_accept)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup = data.get('markup')
    text = data.get('text')
    users = await select_all_users()
    try:
        for i in users:
            await bot.send_message(text=text, chat_id=i.user_id, reply_markup=markup, parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')
    await state.finish()


@dp.callback_query_handler(text='add_inline_button_photo', state=Mailing_photo.Buttons)
async def mailin_button(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        f'Отправьте мне список URL-кнопок в одном сообщении. Пожалуйста, следуйте этому формату:\n\nКнопка 1 | http://example1.com | Кнопка 2 | http://example2.com')
    await Mailing_photo.Buttons_info.set()


@dp.message_handler(state=Mailing_photo.Buttons_info)
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
                await Mailing_photo.Approve.set()
            else:
                await bot.send_photo(photo=photo, caption=caption, reply_markup=markup, chat_id=msg.chat.id,
                                     parse_mode='HTML')
                await msg.answer(text='Для действия нажмите нужную вам кнопку')
                await state.update_data(markup=markup)
                await Mailing_photo.Approve.set()
        except:
            await msg.answer('Вы не правильно написали кнопки')


@dp.message_handler(state=Mailing_photo.Approve)
async def mail_aprove(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        await msg.answer(text='Вы действительно хотите отправить', reply_markup=approve_keyboard)
        await Mailing_photo.Approve_accept.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


@dp.message_handler(state=Mailing_photo.Buttons)
async def mailin_no_button(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        await msg.answer('Вы действительно хотите отправить', reply_markup=approve_keyboard)
        await Mailing_photo.Approve_without_buttons.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


@dp.callback_query_handler(text='accept_mailing', state=Mailing_photo.Approve_accept)
async def mailing_appo(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup = data.get('markup')
    caption = data.get('caption')
    photo = data.get('photo')
    # Сделать рассылку по пользователям
    users = await select_all_users()
    try:
        for i in users:
            if caption == None:
                await bot.send_photo(photo=photo, reply_markup=markup, chat_id=i.user_id, parse_mode='HTML')
            else:
                await bot.send_photo(photo=photo, caption=caption, reply_markup=markup, chat_id=i.user_id,
                                     parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')

    await state.finish()


@dp.callback_query_handler(text='accept_mailing', state=Mailing_photo.Approve_without_buttons)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photo = data.get('photo')
    caption = data.get('caption')
    # Сделать рассылку по пользователям
    users = await select_all_users()
    try:
        for i in users:
            if caption == None:
                await bot.send_photo(chat_id=i.user_id, photo=photo, parse_mode='HTML')
            else:
                await bot.send_photo(chat_id=i.user_id, photo=photo, caption=caption, parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing_photo.Approve_accept)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing_photo.Approve_without_buttons)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


# ВИДЕО
@dp.callback_query_handler(text='add_inline_button_video', state=Mailing_video.Buttons)
async def mailin_button(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        f'Отправьте мне список URL-кнопок в одном сообщении. Пожалуйста, следуйте этому формату:\n\nКнопка 1 | http://example1.com | Кнопка 2 | http://example2.com')
    await Mailing_video.Buttons_info.set()


@dp.message_handler(state=Mailing_video.Buttons)
async def mailin_no_button(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        await msg.answer('Вы действительно хотите отправить', reply_markup=approve_keyboard)
        await Mailing_video.Approve_without_buttons.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


@dp.message_handler(state=Mailing_video.Buttons_info)
async def mailin_button_info(msg: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
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
        await Mailing_video.Approve.set()
    except:
        await msg.answer('Вы не правильно написали кнопки')


@dp.callback_query_handler(text='accept_mailing', state=Mailing_video.Approve_without_buttons)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    caption = data.get('caption')
    video = data.get('video')
    # Сделать рассылку по пользователям
    users = await select_all_users()
    try:
        for i in users:
            if caption == None:
                await bot.send_video(chat_id=i.user_id, video=video, parse_mode='HTML')
            else:
                await bot.send_video(chat_id=i.user_id, video=video, caption=caption, parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')
    await state.finish()


@dp.message_handler(state=Mailing_video.Approve)
async def mail_aprove(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        await msg.answer(text='Вы действительно хотите отправить', reply_markup=approve_keyboard)
        await Mailing.Approve_accept.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


@dp.callback_query_handler(text='accept_mailing', state=Mailing_video.Approve_accept)
async def mailing_appo(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup = data.get('markup')
    caption = data.get('caption')
    video = data.get('video')
    chat_id = data.get('chat_id')
    # Сделать рассылку по пользователям
    users = await select_all_users()
    try:
        for i in users:
            if caption == None:
                await bot.send_video(video=video, reply_markup=markup, chat_id=i.user_id, parse_mode='HTML')
            else:
                await bot.send_photo(video=video, caption=caption, reply_markup=markup, chat_id=i.user_id,
                                     parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')
    await state.finish()

    await state.finish()


@dp.callback_query_handler(text='accept_mailing', state=Mailing_video.Approve_without_buttons)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    video = data.get('video')
    caption = data.get('caption')
    # Сделать рассылку по пользователям
    users = await select_all_users()
    try:
        for i in users:
            if caption == None:
                await bot.send_video(chat_id=i.user_id, video=video, parse_mode='HTML')
            else:
                await bot.send_video(chat_id=i.user_id, video=video, caption=caption, parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing_video.Approve_accept)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing_video.Approve_without_buttons)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


# Gif
@dp.callback_query_handler(text='add_inline_button_gif', state=Mailing_gif.Buttons)
async def mailin_button(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        f'Отправьте мне список URL-кнопок в одном сообщении. Пожалуйста, следуйте этому формату:\n\nКнопка 1 | http://example1.com | Кнопка 2 | http://example2.com')
    await Mailing_gif.Buttons_info.set()


@dp.message_handler(state=Mailing_gif.Buttons)
async def mailin_no_button(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        await msg.answer('Вы действительно хотите отправить', reply_markup=approve_keyboard)
        await Mailing_gif.Approve_without_buttons.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


@dp.message_handler(state=Mailing_gif.Buttons_info)
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
            await Mailing_gif.Approve.set()
        else:
            await bot.send_animation(animation=gif, caption=caption, reply_markup=markup, chat_id=msg.chat.id,
                                     parse_mode='HTML')
            await msg.answer(text='Для действия нажмите нужную вам кнопку')
            await state.update_data(markup=markup)
            await Mailing_gif.Approve.set()
    except:
        await msg.answer('Вы не правильно написали кнопки')


@dp.callback_query_handler(text='accept_mailing', state=Mailing_gif.Approve_without_buttons)
async def mailing_apporve(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    gif = data.get('gif')
    caption = data.get('caption')
    # Сделать рассылку по пользователям
    users = await select_all_users()
    try:
        for i in users:
            if caption == None:
                await bot.send_animation(chat_id=i.user_id, animation=gif, parse_mode='HTML')
            else:
                await bot.send_animation(chat_id=i.user_id, animation=gif, caption=caption, parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')
    await state.finish()


@dp.message_handler(state=Mailing_gif.Approve)
async def mail_aprove(msg: types.Message, state: FSMContext):
    if msg.text == 'Далее':
        await msg.answer(text='Вы действительно хотите отправить', reply_markup=approve_keyboard)
        await Mailing_gif.Approve_accept.set()
    elif msg.text == 'Отменить':
        await msg.answer('Отменено', reply_markup=start_admin)
        await state.finish()


@dp.callback_query_handler(text='accept_mailing', state=Mailing_gif.Approve_accept)
async def mailing_appo(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup = data.get('markup')
    caption = data.get('caption')
    gif = data.get('gif')
    # Сделать рассылку по пользователям
    users = await select_all_users()
    try:
        for i in users:
            if caption == None:
                await bot.send_animation(animation=gif, reply_markup=markup, chat_id=i.user_id, parse_mode='HTML')
            else:
                await bot.send_animation(animation=gif, caption=caption, reply_markup=markup, chat_id=i.user_id,
                                         parse_mode='HTML')
    except:
        pass
    await call.message.answer('Рассылка закончена')
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing_gif.Approve_accept)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing_gif.Approve_without_buttons)
async def mailing_apporve_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=start_admin)
    await state.finish()
