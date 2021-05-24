
from handlers import (add_cafe, add_cafe_name, rate_taste, rate_supply, rate_service, rate_interior, rate_atmosphere, rate_details,
                      add_point, add_comment, dont_know)

from telegram.ext import MessageHandler, Filters, ConversationHandler


ADD_CAFE = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^(Хочу оценить заведение)'), add_cafe)],
    states={
        'add_cafe_name': [MessageHandler(Filters.text, add_cafe_name)],
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
                              dont_know)]
    )
