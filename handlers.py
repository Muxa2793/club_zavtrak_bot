import logging
import re
from db import db, find_rate_cafe, find_unrate_cafe
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ConversationHandler
from settings import HELP
from utils import main_keyboard, show_rating_keyboard


def greet_user(update, context):
    logging.info('Вызван /start')

    update.message.reply_text('Вас приветствует club_zavtrak_bot. Вы вызвали команду /start.\n'
                              'Бот создан для оценки ресторанных заведений по методике "скури" и '
                              'ведения базы посещённых ресторанов.',
                              reply_markup=main_keyboard())


def help_user(update, context):
    logging.info('Вызван /help')

    update.message.reply_text(HELP)


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
                cafe_list.append(cafe['cafe_name'] + ' - ' + cafe['about_cafe']['summ'])
                x.append(cafe['cafe_name'])
            cafe_list_string = '\n'.join(cafe_list).lower().capitalize()
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
            for cafe in cafe_find:
                cafe_list.append('- ' + cafe['cafe_name'])
            cafe_list_string = '\n'.join(cafe_list).lower().capitalize()
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='HTML',
                                     text=f'Список не оцененных заведений:\n'
                                          f'{cafe_list_string}')


def rate_or_show_cafe(update, context):
    query = update.inline_query.query
    match_more = re.match(r'Подробнее:', query)
    if match_more.group(0) == 'Подробнее:':
        id_num = 0
        results = []
        for cafe_name in context.user_data['cafe_name']:
            id_num += 1
            article = InlineQueryResultArticle(
                id=str(id_num), title=cafe_name.capitalize(),
                description='Посмотреть оценку',
                input_message_content=InputTextMessageContent(message_text=f'Хочу узнать оценку '
                                                                           f'{cafe_name.capitalize()}'))
            results.append(article)
        update.inline_query.answer(results, cache_time=1)

'''''
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
'''

