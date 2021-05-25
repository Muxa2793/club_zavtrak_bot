from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([['Добавить заведение'],
                               ['Посещённые заведения'],
                               ['Не посещённые заведения']],
                               resize_keyboard=True)


def rate_keyboard():
    return ReplyKeyboardMarkup([['Пропустить', 'Заново', 'Выйти']], resize_keyboard=True)


def rate_end_keyboard():
    return ReplyKeyboardMarkup([['Закончить', 'Заново']], resize_keyboard=True)


def show_rating_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Подробнее', switch_inline_query_current_chat='Подробнее:'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
