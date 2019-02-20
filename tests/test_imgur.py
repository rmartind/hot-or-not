import unittest
import configparser
from hot_or_not.imgur import Imgur


config = configparser.ConfigParser()
config.read('../hot_or_not/config.ini')

client_id = config['IMGUR_CLIENT']['CLIENT_ID']
girl_album = config['IMGUR_CLIENT']['GIRL_HASH']


class TestAlbum(unittest.TestCase):
    def setUp(self):
        self.imgur = Imgur(client_id)

    def test_girl_album(self):
        self.imgur.album(girl_album)


class TestAlbumImages(unittest.TestCase):
    def setUp(self):
        self.imgur = Imgur(client_id)

    def test_girl_images(self):
        self.imgur.album_images(girl_album)


class TestAlbumImageCount(unittest.TestCase):
    def setUp(self):
        pass


class TestAlbumImage(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
