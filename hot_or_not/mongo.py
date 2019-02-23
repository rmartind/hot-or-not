import pymongo
import random
import asyncio
from decimal import Decimal
from pymongo import MongoClient
from imgur import Imgur


class Mongo(object):
    def __init__(self, imgur_id):
        """Initializes Mongo.

        Args:
            imgur_id: id to authorize the imgur API.
        """
        self._imgur_client_id = imgur_id
        self._imgur = Imgur(self._imgur_client_id)
        self._client = MongoClient('mongodb://127.0.0.1:27017/')
        self._db = self._client.hotornot

    def random_girl(self):
        """Fetches a random girl from girls collection.

        Fetches a random girl from the girls collection by limited the result to one
        and skipping over a random number of integers that is equal to or less than 
        the number of elements in the collection.

        Returns:
            A dict object representing the random girl fetched 
            from the collection.
        """
        return [result for result in self._db.girls.find().limit(1) \
            .skip(random.randrange(self._db.girls.count()))][0]

    def random_boy(self):
        """Fetches a random boy from boys collection.

        Fetches a random boy from the boys collection by limited the result to one
        and skipping over a random number of integers that is equal to or less than 
        the number of elements in the collection.

        Returns:
            A dict object representing the random boy fetched 
            from the collection.
        """
        return [result for result in self._db.boys.find().limit(1) \
            .skip(random.randrange(self._db.boys.count()))][0]

    def upload_album(self, hash, girl=True):
        """Uploads image data to a MongoDB collection.

        Fetches an album based on a hash value from the Imgur API and
        formats the hash and link into a dictionary with a default rating
        and vote count for each image in the album. The images are placed into
        a MongoDB collection corresponding to the supplied gender.

        Args:
            hash: A hash associated with an Imgur album.
            girl: gender of the album photos.
        """
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
        """Updates a girl with a new average rating.

        Given the associated girl image hash, the new rating is applied to the 
        count and old rating to get a total average. The new average is then 
        updated into the corresponding MongoDB document.

        Args:
            hash: A hash belong to a girl's image.
            new_rate: A new rating supplied by a user.
        """
        image = self._db.girls.find_one({'_id': hash})
        total_average = self.average(image['rating'], new_rate, image['count'])

        self._db.girls.find_one_and_update(
            {'_id': hash}, {'$inc': {'count': 1},
                            '$set': {'rating': total_average}},
            return_document=pymongo.ReturnDocument.AFTER)

    def update_boy(self, hash, new_rate):
        """Updates a girl with a new average rating.

        Given the associated girl image hash, the new rating is applied to the 
        count and old rating to get a total average. The new average is then 
        updated into the corresponding MongoDB document.

        Args:
            hash: A hash belong to a girl's image.
            new_rate: A new rating supplied by a user.
        """
        image = self._db.boys.find_one({'_id': hash})
        total_average = self.average(image['rating'], new_rate, image['count'])

        self._db.boys.find_one_and_update(
            {'_id': hash}, {'$inc': {'count': 1},
                            '$set': {'rating': total_average}},
            return_document=pymongo.ReturnDocument.AFTER)

    def top_girls(self):
        """Returns top 5 girls based on rating."""
        return [girl for girl in self._db.girls.find().sort('rating', pymongo.DESCENDING).limit(5)]

    def top_boys(self):
        """Returns top 5 guys based on rating."""
        return [boy for boy in self._db.boys.find().sort('rating', pymongo.DESCENDING).limit(5)]

    @staticmethod
    def average(old_rating, new_rating, count):
        """Returns a new incremental average."""
        return float(round(Decimal((old_rating * count + new_rating) / (count + 1)), 1))
