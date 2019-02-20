import requests


API_URL = 'https://api.imgur.com/3/'


class Imgur(object):
    def __init__(self, client_id, client_secret=None):
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, id):
        self._client_id = id

    @property
    def client_secret(self):
        return self._client_id

    @client_secret.setter
    def client_secret(self, id):
        self._client_id = id

    def send(self, endpoint, payload={}):
        url = API_URL + endpoint
        headers = {
            'Authorization': 'Client-ID ' + self._client_id
        }
        response = requests.request(
            'GET', url, headers=headers, data=payload, allow_redirects=False, timeout=None)
        return response.json()

    def album(self, album_hash):
        return self.send('album/' + album_hash)

    def album_images(self, album_hash):
        return self.send('album/' + album_hash + '/images')

    def album_image(self, album_hash, image_hash):
        return self.send('album/' + album_hash + '/image/' + image_hash)
