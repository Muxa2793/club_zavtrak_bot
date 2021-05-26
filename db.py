from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)
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
        return False
    else:
        return db.cafe.find({'chat_id': chat_id, 'rate': False})


def find_rate_cafe(db, chat_id):
    cafe_list = db.cafe.find_one({'chat_id': chat_id, 'rate': True})
    if cafe_list is None:
        return False
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
