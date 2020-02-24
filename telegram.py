import requests
import os

path = os.path.dirname(__file__)
key_file = open(path + '/.key', 'r')
KEY = key_file.read()
key_file.close()

BASE_PATH = 'https://api.telegram.org/bot' + KEY + '/'


def get_me():
    return requests.get(BASE_PATH + 'getMe').json()


def send_message(msg):
    return requests.post(BASE_PATH + 'sendMessage', dict(chat_id=530378414, text=msg)).json()


def send_image(image, caption='', silent=False):
    return requests.post(BASE_PATH + 'sendPhoto', dict(chat_id=530378414, photo=image, caption=caption, disable_notification=silent))
