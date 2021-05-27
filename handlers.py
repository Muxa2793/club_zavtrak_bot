import logging
import re
from db import db, find_rate_cafe, find_unrate_cafe, get_about_cafe
from telegram import InlineQueryResultArticle, InputTextMessageContent
from settings import HELP
from utils import main_keyboard, show_rating_keyboard, rating_keyboard, edit_keyboard


def greet_user(update, context):
    logging.info('Вызван /start')

    update.message.reply_text('Вас приветствует club_zavtrak_bot. Вы вызвали команду /start.\n'
                              'Бот создан для оценки ресторанных заведений по методике <b>"скури"</b> и '
                              'ведения базы посещённых ресторанов.',
                              reply_markup=main_keyboard(),
                              parse_mode='HTML')


def help_user(update, context):
    logging.info('Вызван /help')

    update.message.reply_text(HELP, parse_mode='HTML')


def show_cafe(update, context):
    text = update.message.text
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    if text == 'Посещённые заведения':
        cafe_find = find_rate_cafe(db, update.effective_chat.id)
        if cafe_find is False:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Cписок посещённых заведений пуст.')
        else:
            cafe_list = []
            context.user_data['cafe_name'] = []
            x = context.user_data['cafe_name']
            for cafe in cafe_find:
                cafe_list.append(cafe['cafe_name'].lower().capitalize() + ' - ' + cafe['about_cafe']['summ'])
                x.append(cafe['cafe_name'])
            cafe_list_string = '\n'.join(cafe_list)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='HTML',
                                     text=f'Список посещённых заведений:\n'
                                          f'{cafe_list_string}',
                                     reply_markup=show_rating_keyboard())
    elif text == 'Не посещённые заведения':
        cafe_find = find_unrate_cafe(db, update.effective_chat.id)
        if cafe_find is False:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Вы ещё не оценили ни одного места')
        else:
            cafe_list = []
            context.user_data['cafe_name'] = []
            x = context.user_data['cafe_name']
            for cafe in cafe_find:
                cafe_list.append('- ' + cafe['cafe_name'].lower().capitalize())
                x.append(cafe['cafe_name'])
            cafe_list_string = '\n'.join(cafe_list)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='HTML',
                                     text=f'Список не оценённых заведений:\n'
                                          f'{cafe_list_string}',
                                          reply_markup=rating_keyboard())


def rate_or_show_cafe(update, context):
    query = update.inline_query.query
    try:
        match_more = re.match(r'Подробнее:|Оценить:|Удалить:|Редактировать:', query)
    except AttributeError:
        pass
    try:
        if match_more.group(0) == 'Подробнее:':
            id_num = 0
            results = []
            cafe_list = context.user_data['cafe_name']
            r = re.compile(f'{query[11:].lower()}.*')
            cafe_list_filter = list(filter(r.match, cafe_list))
            for cafe_name in cafe_list_filter:
                id_num += 1
                article = InlineQueryResultArticle(
                            id=str(id_num), title=cafe_name.capitalize(),
                            description='Посмотреть оценку',
                            input_message_content=InputTextMessageContent(message_text=f'Хочу узнать оценку '
                                                                                       f'{cafe_name.capitalize()}'))
                results.append(article)
            update.inline_query.answer(results, cache_time=1)
        elif match_more.group(0) == 'Оценить:':
            id_num = 0
            results = []
            cafe_list = context.user_data['cafe_name']
            r = re.compile(f'{query[9:].lower()}.*')
            cafe_list_filter = list(filter(r.match, cafe_list))
            for cafe_name in cafe_list_filter:
                id_num += 1
                article = InlineQueryResultArticle(
                            id=str(id_num), title=cafe_name.capitalize(),
                            description='Оценить заведение',
                            input_message_content=InputTextMessageContent(message_text=f'Хочу оценить заведение '
                                                                                       f'{cafe_name.capitalize()}'))
                results.append(article)
            update.inline_query.answer(results, cache_time=1)
        elif match_more.group(0) == 'Удалить:':
            id_num = 0
            results = []
            cafe_list = context.user_data['cafe_name']
            r = re.compile(f'{query[9:].lower()}.*')
            cafe_list_filter = list(filter(r.match, cafe_list))
            for cafe_name in cafe_list_filter:
                id_num += 1
                article = InlineQueryResultArticle(
                            id=str(id_num), title=cafe_name.capitalize(),
                            description='Удалить заведение из списка',
                            input_message_content=InputTextMessageContent(message_text=f'Хочу удалить заведение '
                                                                                       f'{cafe_name.capitalize()}'))
                results.append(article)
            update.inline_query.answer(results, cache_time=1)
        elif match_more.group(0) == 'Редактировать:':
            cafe_name = context.user_data['cafe_name']
            results = [
                InlineQueryResultArticle(
                        id='1', title=cafe_name.capitalize(),
                        description='Оценить заведение заново',
                        input_message_content=InputTextMessageContent(message_text=f'Хочу оценить заведение '
                                                                                   f'{cafe_name.capitalize()}')),
                InlineQueryResultArticle(
                        id='2', title=cafe_name.capitalize(),
                        description='Удалить заведение',
                        input_message_content=InputTextMessageContent(message_text=f'Хочу удалить заведение '
                                                                                   f'{cafe_name.capitalize()}'))]
            update.inline_query.answer(results, cache_time=1)
            context.user_data['cafe_name'] = cafe_name
    except (TypeError, AttributeError):
        pass


def show_rating_or_rate_cafe(update, context):
    text = update.message.text
    text = text.split(' ')
    cafe_name = ' '.join(text[3:])
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    if text[0:3] == ['Хочу', 'узнать', 'оценку']:
        about_cafe = get_about_cafe(db, update.effective_chat.id, cafe_name)
        context.user_data['cafe_name'] = about_cafe['cafe_name']
        taste = about_cafe['about_cafe']['taste']
        supply = about_cafe['about_cafe']['supply']
        service = about_cafe['about_cafe']['service']
        interior = about_cafe['about_cafe']['interior']
        atmosphere = about_cafe['about_cafe']['atmosphere']
        details = about_cafe['about_cafe']['details']
        point = about_cafe['about_cafe']['point']
        comment = about_cafe['about_cafe']['comment']
        summ = about_cafe['about_cafe']['summ']
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Название: <b>{cafe_name}</b>\n'
                                      f'Вкус - <b>{taste}</b>\n'
                                      f'Подача - <b>{supply}</b>\n'
                                      f'Сервис - <b>{service}</b>\n'
                                      f'Интерьер - <b>{interior}</b>\n'
                                      f'Атмосфера - <b>{atmosphere}</b>\n'
                                      f'Детали - <b>{details}</b>\n'
                                      f'Дополнительный балл - <b>{point}</b>\n'
                                      f'Комментарий: <b>{comment}</b>\n\n'
                                      f'<b>Итого: {summ}</b>',
                                 parse_mode='HTML',
                                 reply_markup=edit_keyboard(cafe_name))
    elif text[0:3] == ['Хочу', 'удалить', 'заведение']:
        pass
