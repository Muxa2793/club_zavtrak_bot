from telegram.ext import ConversationHandler
from utils import rate_keyboard, main_keyboard, rate_again_keyboard
from db import db, get_about_cafe, change_rate_status, add_cafe_rate


def rate_cafe(update, context):
    update.message.text
    text = update.message.text
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    text = text.split()
    context.user_data['cafe_name'] = ' '.join(text[3:])
    cafe_name = context.user_data['cafe_name']
    find_cafe = get_about_cafe(db, update.effective_chat.id, cafe_name)
    if find_cafe['rate'] is False:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode='HTML',
                                 text=f'Оцените вкус еды в <b>"{cafe_name}"</b> от 0 до 1.5',
                                 reply_markup=rate_keyboard())
        return 'rate_taste'
    elif find_cafe['rate'] is True:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode='HTML',
                                 text=f'Вы уже оценили заведение "{cafe_name}". Хотите оценить ещё раз?',
                                 reply_markup=rate_again_keyboard(cafe_name))
        return 'rate_again'


def rate_repeat(update, context):
    if update.message.text == 'Выйти':
        return exit_rating(update, context)
    cafe_name = context.user_data['cafe_name']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             parse_mode='HTML',
                             text=f'Оцените вкус еды в <b>"{cafe_name}"</b> от 0 до 1.5')
    return 'rate_taste'


def rate_taste(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['taste'] = 'Без оценки'
        update.message.reply_text(f'Оцените подачу в <b>"{cafe_name}"</b> от 0 до 1.5',
                                  parse_mode='HTML')
        return 'rate_supply'
    elif update.message.text == 'Заново':
        return rate_repeat(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['taste'] = rating
                update.message.reply_text(f'Оцените подачу в <b>"{cafe_name}"</b> от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_supply'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
                return 'rate_taste'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
            return 'rate_taste'


def rate_supply(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['supply'] = 'Без оценки'
        update.message.reply_text(f'Оцените сервис в <b>"{cafe_name}"</b> от 0 до 1.5',
                                  parse_mode='HTML')
        return 'rate_service'
    elif update.message.text == 'Заново':
        return rate_repeat(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['supply'] = rating
                update.message.reply_text(f'Оцените сервис в <b>"{cafe_name}"</b> от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_service'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
                return 'rate_supply'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
            return 'rate_supply'


def rate_service(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['service'] = 'Без оценки'
        update.message.reply_text(f'Оцените интерьер в <b>"{cafe_name}"</b> от 0 до 1.5',
                                  parse_mode='HTML')
        return 'rate_interior'
    elif update.message.text == 'Заново':
        return rate_repeat(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['service'] = rating
                update.message.reply_text(f'Оцените интерьер в <b>"{cafe_name}"</b> от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_interior'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_service'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1.5',
                                      parse_mode='HTML')
            return 'rate_service'


def rate_interior(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['interior'] = 'Без оценки'
        update.message.reply_text(f'Оцените атмосферу в <b>"{cafe_name}"</b> от 0 до 1.5',
                                  parse_mode='HTML')
        return 'rate_atmosphere'
    elif update.message.text == 'Заново':
        return rate_repeat(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['interior'] = rating
                update.message.reply_text(f'Оцените атмосферу в <b>"{cafe_name}"</b> от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_atmosphere'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
                return 'rate_interior'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
            return 'rate_interior'


def rate_atmosphere(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['atmosphere'] = 'Без оценки'
        update.message.reply_text(f'Оцените маленькие детали в <b>"{cafe_name}"</b> от 0 до 1.5',
                                  parse_mode='HTML')
        return 'rate_details'
    elif update.message.text == 'Заново':
        return rate_repeat(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['atmosphere'] = rating
                update.message.reply_text(f'Оцените маленькие детали в <b>"{cafe_name}"</b> от 0 до 1.5',
                                          parse_mode='HTML')
                return 'rate_details'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
                return 'rate_atmosphere'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1.5')
            return 'rate_atmosphere'


def rate_details(update, context):
    rating = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['details'] = 'Без оценки'
        update.message.reply_text(f'Добавьте дополнительный балл для <b>"{cafe_name}"</b> от 0 до 1 по желанию',
                                  parse_mode='HTML')
        return 'add_point'
    elif update.message.text == 'Заново':
        return rate_repeat(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(rating) <= 1.5:
                context.user_data['details'] = rating
                summ = 0
                values = context.user_data.values()
                list_values = list(values)
                for rating in list_values[1:7]:
                    try:
                        summ = summ + float(rating)
                    except ValueError:
                        summ = 'Без оценки'
                update.message.reply_text(f'Итого: <b>{summ}</b>\nДобавьте дополнительный балл для'
                                          f'<b>"{cafe_name}"</b> от 0 до 1 по желанию',
                                          parse_mode='HTML')
                return 'add_point'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1')
                return 'rate_details'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1')
            return 'rate_details'


def add_point(update, context):
    point = update.message.text
    cafe_name = context.user_data['cafe_name']
    if update.message.text == 'Пропустить':
        context.user_data['point'] = 'Без оценки'
        update.message.reply_text(f'Добавьте комментарий для <b>"{cafe_name}"</b>',
                                  parse_mode='HTML')
        return 'add_comment'
    elif update.message.text == 'Заново':
        return rate_repeat(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        try:
            if 0 <= float(point) <= 1:
                context.user_data['point'] = point
                update.message.reply_text(f'Добавьте комментарий для <b>"{cafe_name}"</b>',
                                          parse_mode='HTML')
                return 'add_comment'
            else:
                update.message.reply_text('Пожалуйста, введите число от 0 до 1')
                return 'add_point'
        except ValueError:
            update.message.reply_text('Пожалуйста, введите число от 0 до 1')
            return 'add_point'


def add_comment(update, context):
    if update.message.text == 'Пропустить':
        context.user_data['comment'] = 'Без комментариев'
        comment = context.user_data['comment']
    elif update.message.text == 'Заново':
        return rate_repeat(update, context)
    elif update.message.text == 'Выйти':
        return exit_rating(update, context)
    else:
        comment = update.message.text
        context.user_data['comment'] = comment
    cafe_name = context.user_data['cafe_name']
    taste = context.user_data['taste']
    supply = context.user_data['supply']
    service = context.user_data['service']
    interior = context.user_data['interior']
    atmosphere = context.user_data['atmosphere']
    details = context.user_data['details']
    point = context.user_data['point']
    summ = 0
    values = context.user_data.values()
    list_values = list(values)
    for rating in list_values[1:8]:
        try:
            summ = summ + float(rating)
        except ValueError:
            continue
    if summ == 0:
        summ = 'Без оценки'
    change_rate_status(db, update.effective_chat.id, cafe_name)
    add_cafe_rate(db, update.effective_chat.id, context.user_data, str(summ))
    update.message.reply_text(f'Название: <b>{cafe_name}</b>\n'
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
                              reply_markup=main_keyboard())
    return ConversationHandler.END


def rate_again(update, context):
    answer = update.message.text
    cafe_name = context.user_data['cafe_name']
    if answer == f'Оценить заново заведение {cafe_name}':
        change_rate_status(db, update.effective_chat.id, cafe_name)
        return rate_cafe(update, context)
    elif answer == 'Выйти':
        update.message.reply_text('До свидания!',
                                  reply_markup=main_keyboard())
        return ConversationHandler.END


def exit_rating(update, context):
    update.message.reply_text('Оценка удалена. До свидания!',
                              reply_markup=main_keyboard())
    context.user_data.clear()
    return ConversationHandler.END


def rate_dont_know(update, context):
    update.message.reply_text('Я вас не понимаю')
