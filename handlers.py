import logging
from db import db, find_cafe
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from settings import HELP
from utils import rate_keyboard

CAFE_ICON = 'https://i.ibb.co/pv8RDPL/cafe.png'
INFO_ICON = 'https://i.ibb.co/4NLgGyD/rating.png'


def greet_user(update, context):
    logging.info('Вызван /start')

    update.message.reply_text('Вас приветствует club_zavtrak_bot. Вы вызвали команду /start.\n'
                              'Бот создан для оценки ресторанных заведений по методике "скури" и '
                              'ведения базы посещённых ресторанов.')


def help_user(update, context):
    logging.info('Вызван /help')

    update.message.reply_text(HELP)


def add_or_rate_cafe(update, context):
    query = update.inline_query.query
    if query == '':
        query = 'cafe_name'
    cafe_name = query
    cafe = find_cafe(db, cafe_name)
    if cafe is False:
        cafe = query

    results = [
        InlineQueryResultArticle(
            id='1', title="Оценить заведение:",
            description=f'{query.capitalize()}',
            input_message_content=InputTextMessageContent(message_text=f'Хочу оценить заведение {query.capitalize()}'),
            thumb_url=CAFE_ICON, thumb_width=48, thumb_height=48),
        InlineQueryResultArticle(
            id='2', title="Показать оценку:",
            description=f'{cafe.capitalize()}',
            input_message_content=InputTextMessageContent(message_text=f'Хочу показать оценку {cafe.capitalize()}'),
            thumb_url=INFO_ICON, thumb_width=48, thumb_height=48
        )]
    update.inline_query.answer(results, cache_time=1)


def add_cafe(update, context):
    text = update.message.text
    if text == 'Заново':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Напишите название заведения:',
                                 reply_markup=rate_keyboard())
        return 'add_cafe_name'
    if 'Cafe_name' in text:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='После @club_zavtrak_bot напишите название заведения')
        return ConversationHandler.END
    else:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        text = text.split()
        context.user_data['cafe_name'] = text[3:]
        cafe_name = context.user_data['cafe_name']
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode='HTML',
                                 text=f'Оцените вкус еды в <b>"{cafe_name}"</b> от 0 до 1.5',
                                 reply_markup=rate_keyboard())
        return 'rate_taste'


def add_cafe_name(update, context):
    if update.message.text == 'Выйти':
        return exit_rating(update, context)
    cafe_name = update.message.text
    context.user_data['cafe_name'] = cafe_name
    context.bot.send_message(chat_id=update.effective_chat.id,
                             parse_mode='HTML',
                             text=f'Оцените вкус еды в <b>"{cafe_name}"</b> от 0 до 1.5')
    return 'rate_taste'


def rate_taste(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['taste'] = 'Без оценки'
        update.message.reply_text(f'Оцените подачу в <b>"{cafe_name}"</b> от 0 до 1.5',
                                  parse_mode='HTML')
        return 'rate_supply'
    elif update.message.text == 'Заново':
        return add_cafe(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['taste'] = rating
                update.message.reply_text(f'Оцените подачу в <b>"{cafe_name}"</b> от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_supply'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
                return 'rate_taste'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
            return 'rate_taste'


def rate_supply(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['supply'] = 'Без оценки'
        update.message.reply_text(f'Оцените сервис в <b>"{cafe_name}"</b> от 0 до 1.5',
                                  parse_mode='HTML')
        return 'rate_service'
    elif update.message.text == 'Заново':
        return add_cafe(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['supply'] = rating
                update.message.reply_text(f'Оцените сервис в <b>"{cafe_name}"</b> от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_service'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
                return 'rate_supply'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
            return 'rate_supply'


def rate_service(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['service'] = 'Без оценки'
        update.message.reply_text(f'Оцените интерьер в <b>"{cafe_name}"</b> от 0 до 1.5',
                                  parse_mode='HTML')
        return 'rate_interior'
    elif update.message.text == 'Заново':
        return add_cafe(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['service'] = rating
                update.message.reply_text(f'Оцените интерьер в <b>"{cafe_name}"</b> от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_interior'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_service'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1.5',
                                      parse_mode='HTML')
            return 'rate_service'


def rate_interior(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['interior'] = 'Без оценки'
        update.message.reply_text(f'Оцените атмосферу в <b>"{cafe_name}"</b> от 0 до 1.5',
                                  parse_mode='HTML')
        return 'rate_atmosphere'
    elif update.message.text == 'Заново':
        return add_cafe(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['interior'] = rating
                update.message.reply_text(f'Оцените атмосферу в <b>"{cafe_name}"</b> от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_atmosphere'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
                return 'rate_interior'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
            return 'rate_interior'


def rate_atmosphere(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['atmosphere'] = 'Без оценки'
        update.message.reply_text(f'Оцените маленькие детали в <b>"{cafe_name}"</b> от 0 до 1.5',
                                  parse_mode='HTML')
        return 'rate_details'
    elif update.message.text == 'Заново':
        return add_cafe(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['atmosphere'] = rating
                update.message.reply_text(f'Оцените маленькие детали в <b>"{cafe_name}"</b> от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_details'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
                return 'rate_atmosphere'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
            return 'rate_atmosphere'


def rate_details(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['details'] = 'Без оценки'
        update.message.reply_text(f'Добавьте дополнительный балл для <b>"{cafe_name}"</b> от 0 до 1 по желанию',
                                  parse_mode='HTML')
        return 'add_point'
    elif update.message.text == 'Заново':
        return add_cafe(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['details'] = rating
                update.message.reply_text(f'Добавьте дополнительный балл для <b>"{cafe_name}"</b> '
                                          'от 0 до 1 по желанию',
                                          parse_mode='HTML')
                return 'add_point'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1')
                return 'rate_details'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1')
            return 'rate_details'


def add_point(update, context):
    point = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['point'] = 'Без оценки'
        update.message.reply_text(f'Добавьте комментарий для <b>"{cafe_name}"</b>',
                                  parse_mode='HTML')
        return 'add_comment'
    elif update.message.text == 'Заново':
        return add_cafe(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(point) <= 1:
                context.user_data['point'] = point
                update.message.reply_text(f'Добавьте комментарий для <b>"{cafe_name}"</b>',
                                          parse_mode='HTML')
                return 'add_comment'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1')
                return 'rate_point'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1')
            return 'rate_point'


def add_comment(update, context):
    if update.message.text == 'Пропустить':
        context.user_data['comment'] = 'Без комментариев'
        comment = context.user_data['comment']
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        comment = update.message.text
        context.user_data['comment'] = comment
    cafe_name = context.user_data['cafe_name']
    taste = context.user_data['taste']
    supply = context.user_data['supply']
    service = context.user_data['service']
    interior = context.user_data['interior']
    atmosphere = context.user_data['atmosphere']
    details = context.user_data['details']
    point = context.user_data['point']
    summ = 0
    values = context.user_data.values()
    list_values = list(values)
    for rating in list_values[1:8]:
        try:
            summ = summ + float(rating)
        except ValueError:
            continue
    if summ == 0:
        summ = 'Без оценки'
    update.message.reply_text(f'Название: <b>{cafe_name}</b>\n'
                              f'Вкус - <b>{taste}</b>\n'
                              f'Подача - <b>{supply}</b>\n'
                              f'Сервис - <b>{service}</b>\n'
                              f'Интерьер - <b>{interior}</b>\n'
                              f'Атмосфера - <b>{atmosphere}</b>\n'
                              f'Детали - <b>{details}</b>\n'
                              f'Дополнительный балл - <b>{point}</b>\n'
                              f'Комментарий: <b>{comment}</b>\n\n'
                              f'<b>Итого: {summ}</b>',
                              parse_mode='HTML')
    context.user_data.clear()
    return ConversationHandler.END


def exit_rating(update, context):
    update.message.reply_text('Оценка удалена. До свидания!',
                              reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


def dont_know(update, context):
    update.message.reply_text('Я вас не понимаю')
