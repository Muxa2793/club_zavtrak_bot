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
        }
        db.cafe.insert_one(cafe)
        return cafe
    else:
        return True


def find_cafe(db, cafe_name):
    if cafe_name == '':
        return False
    cafe_list = db.cafe.find_one({'cafe_name': {'$regex': f'^{cafe_name.lower()}'}})
    if cafe_list is None:
        return False
    else:
        cafe_name = cafe_list['cafe_name']
        return cafe_name
