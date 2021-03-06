import certifi

import settings

from pymongo import MongoClient


client = MongoClient(settings.MONGO_LINK, tlsCAFile=certifi.where())
db = client[settings.MONGO_DB]


def add_cafe_in_list(db, chat_id, cafe_name):
    cafe = db.cafe.find_one({'chat_id': chat_id, 'cafe_name': cafe_name.lower()})
    if not cafe:
        cafe = {
            'chat_id': chat_id,
            'cafe_name': cafe_name.lower(),
            'rate': False,
            'about_cafe': {'taste': 'Без оценки',
                           'supply': 'Без оценки',
                           'service': 'Без оценки',
                           'interior': 'Без оценки',
                           'atmosphere': 'Без оценки',
                           'details': 'Без оценки',
                           'point': 'Без оценки',
                           'comment': 'Без комментариев',
                           'summ': 'Без оценки'}
        }
        db.cafe.insert_one(cafe)
        return cafe
    else:
        return True


def find_unrate_cafe(db, chat_id):
    cafe_list = db.cafe.find_one({'chat_id': chat_id, 'rate': False})
    if cafe_list is None:
        return 'Список пуст'
    else:
        return db.cafe.find({'chat_id': chat_id, 'rate': False})


def find_rate_cafe(db, chat_id):
    cafe_list = db.cafe.find_one({'chat_id': chat_id, 'rate': True})
    if cafe_list is None:
        return 'Список пуст'
    else:
        return db.cafe.find({'chat_id': chat_id, 'rate': True})


def get_about_cafe(db, chat_id, cafe_name):
    return db.cafe.find_one({'chat_id': chat_id, 'cafe_name': cafe_name.lower()})


def change_rate_status(db, chat_id, cafe_name):
    cafe = db.cafe.find_one({'chat_id': chat_id, 'cafe_name': cafe_name.lower()})
    if cafe:
        if cafe['rate'] is True:
            db.cafe.update_one(
                {'_id': cafe['_id']},
                {'$set': {'rate': False}}
            )
        elif cafe['rate'] is False:
            db.cafe.update_one(
                {'_id': cafe['_id']},
                {'$set': {'rate': True}}
            )


def add_cafe_rate(db, chat_id, cafe_data, summ):
    cafe = db.cafe.find_one({'chat_id': chat_id, 'cafe_name': cafe_data['cafe_name'].lower()})
    if cafe:
        db.cafe.update_one(
            {'_id': cafe['_id']},
            {'$set': {'about_cafe': {'taste': cafe_data['taste'],
                                     'supply': cafe_data['supply'],
                                     'service': cafe_data['service'],
                                     'interior': cafe_data['interior'],
                                     'atmosphere': cafe_data['atmosphere'],
                                     'details': cafe_data['details'],
                                     'point': cafe_data['point'],
                                     'comment': cafe_data['comment'],
                                     'summ': summ}}}
        )


def delete_cafe(db, chat_id, cafe_name):
    cafe = db.cafe.find_one({'chat_id': chat_id, 'cafe_name': cafe_name.lower()})
    if cafe:
        db.cafe.remove({'chat_id': chat_id, 'cafe_name': cafe_name.lower()})
        return True
    else:
        return False
