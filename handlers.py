import logging
from db import db, find_cafe
from telegram import InlineQueryResultArticle, InputTextMessageContent
from settings import HELP

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


def add_and_rate_cafe(update, context):
    text = update.message.text
    if 'Cafe_name' in text:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='После @club_zavtrak_bot напишите название заведения')
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             parse_mode='HTML',
                             text='Функция в разработке')
