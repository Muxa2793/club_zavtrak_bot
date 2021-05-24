from telegram import ReplyKeyboardMarkup


def rate_keyboard():
    return ReplyKeyboardMarkup([['Пропустить', 'Заново', 'Выйти']], resize_keyboard=True)


def rate_end_keyboard():
    return ReplyKeyboardMarkup([['Закончить', 'Заново']], resize_keyboard=True)
