
from rating import (rate_cafe, add_cafe_name, rate_taste, rate_supply, rate_service, rate_interior,
                    rate_atmosphere, rate_details, add_point, add_comment, rate_dont_know)

from telegram.ext import MessageHandler, Filters, ConversationHandler
from db import db, add_cafe_in_list

RATE_CAFE = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^(Хочу оценить заведение)'), rate_cafe)],
    states={
        'rate_taste': [MessageHandler(Filters.text, rate_taste)],
        'rate_supply': [MessageHandler(Filters.text, rate_supply)],
        'rate_service': [MessageHandler(Filters.text, rate_service)],
        'rate_interior': [MessageHandler(Filters.text, rate_interior)],
        'rate_atmosphere': [MessageHandler(Filters.text, rate_atmosphere)],
        'rate_details': [MessageHandler(Filters.text, rate_details)],
        'add_point': [MessageHandler(Filters.text, add_point)],
        'add_comment': [MessageHandler(Filters.text, add_comment)]
    },
    fallbacks=[MessageHandler(Filters.text | Filters.regex('^(Хочу оценить заведение)') | Filters.photo |
                              Filters.video | Filters.location | Filters.document,
                              rate_dont_know)]
    )


def add_cafe(update, context):
    update.message.reply_text('Введите название кафе')
    return 'add_cafe_name'


def dont_know(update, context):
    update.message.reply_text('Я вас не понимаю')


def add_cafe_name(update, context):
    cafe_name = update.message.text
    add_cafe = add_cafe_in_list(db, update.effective_chat.id, cafe_name)
    if add_cafe is True:
        update.message.reply_text(f'Заведение <b>{cafe_name}</b> уже есть в списке.', parse_mode='HTML')
    else:
        update.message.reply_text(f'Заведение <b>{cafe_name}</b> добавлено в список.', parse_mode='HTML')
    return ConversationHandler.END


ADD_CAFE = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^(Добавить заведение)'), add_cafe)],
    states={
        'add_cafe_name': [MessageHandler(Filters.text, add_cafe_name)]
    },
    fallbacks=[MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.location | Filters.document,
               dont_know)]
    )
