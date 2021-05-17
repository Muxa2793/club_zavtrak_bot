import logging
import settings

from handlers import greet_user, help_user, add_and_rate_cafe, add_or_rate_cafe
from telegram.ext import (Updater, CommandHandler, InlineQueryHandler, Filters, MessageHandler)

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {
                                'username': settings.PROXY_USERNAME,
                                'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO,
                    datefmt='%d-%m-%y %H:%M:%S')


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(InlineQueryHandler(add_or_rate_cafe, pass_chat_data=True))
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', help_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Хочу оценить заведение)|(Хочу показать оценку)'),
                                  add_and_rate_cafe))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
