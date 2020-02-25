import requests
import os

path = os.path.dirname(__file__)
key_file = open(path + '/.key', 'r')
KEY = key_file.read()
key_file.close()

BASE_PATH = 'https://api.telegram.org/bot' + KEY + '/'


def get_subscribers():
    sub_file = open(path + '/.chats', 'r')
    subs = sub_file.readlines()
    sub_file.close()
    cleaned_values = []
    [cleaned_values.append(int(value.replace("\n", ''))) for value in subs]
    return cleaned_values


def get_me():
    return requests.get(BASE_PATH + 'getMe').json()


def send_message(msg, parse_mode='HTML'):
    responses = []
    for subscriber in get_subscribers():
        responses.append(
            requests.post(BASE_PATH + 'sendMessage', dict(chat_id=subscriber, text=msg, parse_mode=parse_mode)).json())
    return responses


def send_image(image, caption='', parse_mode='HTML', silent=False):
    responses = []
    for subscriber in get_subscribers():
        responses.append(
            requests.post(BASE_PATH + 'sendPhoto', dict(
                chat_id=subscriber,
                parse_mode=parse_mode,
                photo=image,
                caption=caption,
                disable_notification=silent
            )).json())
    return responses


def get_updates():
    update_file = open(path + '/.last_update', 'r')
    offset = update_file.read()
    update_file.close()
    updates = requests.get(BASE_PATH + 'getUpdates', dict(allowed_updates=['message'], offset=offset)).json()
    if len(updates['result']) == 0:
        return updates['result']
    update_file = open(path + '/.last_update', 'w')
    update_file.write(str(updates['result'][-1]['update_id'] + 1))
    update_file.close()
    return updates['result']


def update_subscriptions():
    updates = get_updates()
    for update in updates:
        if update['message']['text'] == '/subscribe':
            subscribe_chat(update['message']['chat']['id'])
        if update['message']['text'] == '/unsubscribe':
            unsubscribe_chat(update['message']['chat']['id'])


def subscribe_chat(chat_id):
    subscriber_file = open(path + '/.chats', 'r')
    current_subscribers = subscriber_file.readlines()
    subscriber_file.close()
    new_chat_id = str(chat_id) + "\n"
    if new_chat_id in current_subscribers:
        return
    chat_file = open(path + '/.chats', 'a')
    chat_file.write(new_chat_id)
    chat_file.close()


def unsubscribe_chat(chat_id):
    subscriber_file = open(path + '/.chats', 'r')
    current_subscribers = subscriber_file.readlines()
    subscriber_file.close()
    new_chat_id = str(chat_id) + "\n"
    new_chat_ids = []
    for current_subscriber in current_subscribers:
        if not new_chat_id == current_subscriber:
            new_chat_ids.append(new_chat_id)
    chat_file = open(path + '/.chats', 'w')
    chat_file.writelines(new_chat_ids)
    chat_file.close()

