import pymongo
import random
import asyncio
from decimal import Decimal
from pymongo import MongoClient
from imgur import Imgur


class Mongo(object):
    def __init__(self, imgur_id):
        self._imgur_client_id = imgur_id
        self._imgur = Imgur(self._imgur_client_id)
        self._client = MongoClient('mongodb://127.0.0.1:27017/')
        self._db = self._client.hotornot

    def random_girl(self):
        return self._db.girls.find().limit(1) \
            .skip(random.randrange(self._db.girls.count()))

    def random_boy(self):
        return self._db.boys.find().limit(1) \
            .skip(random.randrange(self._db.boys.count()))

    def upload_album(self, hash, girl=True):
        images = self._imgur.album_images(hash)['data']
        for image in images:
            doc = {
                '_id': image['id'],
                'rating': 0.0,
                'count': 0,
                'link': image['link']
            }

            try:
                if girl:
                    self._db.girls.insert_one(doc)
                else:
                    self._db.boys.insert_one(doc)
            except pymongo.errors.DuplicateKeyError:
                continue

    def upload_image(self, hash, girl=True):
        pass

    def update_girl(self, hash, new_rate):
        image = self._db.girls.find_one({'_id': hash})
        total_average = self.average(image['rating'], new_rate, image['count'])

        self._db.girls.find_one_and_update(
            {'_id': hash}, {'$inc': {'count': 1},
                            '$set': {'rating': total_average}},
            return_document=pymongo.ReturnDocument.AFTER)

    def update_boy(self, hash, new_rate):
        image = self._db.boys.find_one({'_id': hash})
        total_average = self.average(image['rating'], new_rate, image['count'])

        self._db.boys.find_one_and_update(
            {'_id': hash}, {'$inc': {'count': 1},
                            '$set': {'rating': total_average}},
            return_document=pymongo.ReturnDocument.AFTER)

    @staticmethod
    def average(old_rating, new_rating, count):
        return float(round(Decimal((old_rating * count + new_rating) / (count + 1)), 1))
