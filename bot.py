import logging
import settings

from handlers import greet_user, help_user, show_cafe, rate_or_show_cafe, show_rating_or_rate_cafe
from conv_handler import ADD_CAFE, RATE_CAFE
from telegram.ext import (Updater, CommandHandler, InlineQueryHandler, Filters, MessageHandler)

logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO,
                    datefmt='%d-%m-%y %H:%M:%S')


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    ADD_CAFE
    RATE_CAFE

    dp = mybot.dispatcher
    dp.add_handler(InlineQueryHandler(rate_or_show_cafe, pass_chat_data=True))
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', help_user))
    dp.add_handler(ADD_CAFE)
    dp.add_handler(RATE_CAFE)
    dp.add_handler(MessageHandler(Filters.regex('^((Посещённые заведения)|(Не посещённые заведения))'), show_cafe))
    dp.add_handler(MessageHandler(Filters.regex('^((Хочу узнать оценку)|'
                                                '(Хочу удалить заведение))'), show_rating_or_rate_cafe))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
