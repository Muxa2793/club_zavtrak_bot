from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([['Добавить заведение'],
                               ['Не посещённые заведения'],
                               ['Посещённые заведения']],
                               resize_keyboard=True)


def rate_keyboard():
    return ReplyKeyboardMarkup([['Пропустить', 'Заново', 'Выйти']], resize_keyboard=True)


def rate_end_keyboard():
    return ReplyKeyboardMarkup([['Закончить', 'Заново']], resize_keyboard=True)


def rate_again_keyboard(cafe_name):
    return ReplyKeyboardMarkup([[f'Оценить заново заведение {cafe_name}'],
                                ['Выйти']], resize_keyboard=True)


def show_rating_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Подробнее', switch_inline_query_current_chat='Подробнее: '),
            InlineKeyboardButton('Удалить', switch_inline_query_current_chat='Удалить: ')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def rating_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Оценить', switch_inline_query_current_chat='Оценить: '),
            InlineKeyboardButton('Удалить', switch_inline_query_current_chat='Удалить: ')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def edit_keyboard(cafe_name):
    keyboard = [
        [
            InlineKeyboardButton('Редактировать', switch_inline_query_current_chat=f'Редактировать: {cafe_name}',
                                 resize_keyboard=True)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def cancel_button():
    return ReplyKeyboardMarkup([['Отменить добавление']], resize_keyboard=True)
