import requests
import os

# Get the current path.
path = os.path.dirname(__file__)
# Get the file containing the bot's key.
key_file = open(path + '/.key', 'r')
# Save the key in a variable.
KEY = key_file.read()
key_file.close()

# Define the base path for the telegram bot api.
BASE_PATH = 'https://api.telegram.org/bot' + KEY + '/'


def get_subscribers():
    """
    Returns a list of all subscribers.

    :rtype: list
    """
    sub_file = open(path + '/.chats', 'r')
    subs = sub_file.readlines()
    sub_file.close()
    cleaned_values = []
    [cleaned_values.append(int(value.replace("\n", ''))) for value in subs]
    return cleaned_values


def get_me():
    """
    Gets the bot. This isn't in use but could be used for debugging and testing if the bot works.

    :rtype: dict
    """
    return requests.get(BASE_PATH + 'getMe').json()


def send_message(msg, parse_mode='HTML'):
    """
    Sends a message to all subscribers.

    :param msg: The message to be send
    :param parse_mode: The mode to use for parsing
    :rtype: dict
    """
    responses = []
    for subscriber in get_subscribers():
        responses.append(
            requests.post(BASE_PATH + 'sendMessage', dict(chat_id=subscriber, text=msg, parse_mode=parse_mode)).json())
    return responses


def send_image(image, caption='', parse_mode='HTML', silent=False):
    """
    Sends an image to all subscribers.

    :param image: The url of the image to send
    :param caption: The caption of the image
    :param parse_mode: The parse mode
    :param silent: Specifies if the message should be send silently.
    :rtype: list
    """
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
    """
    Gets all updates since the last call.

    :rtype: list
    """
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
    """
    Checks and updates subscribers.
    """
    updates = get_updates()
    for update in updates:
        if update['message']['text'] == '/subscribe':
            subscribe_chat(update['message']['chat']['id'])
        if update['message']['text'] == '/unsubscribe':
            unsubscribe_chat(update['message']['chat']['id'])


def subscribe_chat(chat_id):
    """
    Subscribes a user based on the chat id.

    :param chat_id: The chat's id
    """
    subscriber_file = open(path + '/.chats', 'r')
    current_subscribers = subscriber_file.readlines()
    subscriber_file.close()
    new_chat_id = str(chat_id) + "\n"
    # Don't add the chat a second time if already present.
    if new_chat_id in current_subscribers:
        return
    chat_file = open(path + '/.chats', 'a')
    chat_file.write(new_chat_id)
    chat_file.close()


def unsubscribe_chat(chat_id):
    """
    Unsubscribe a chat id from getting further messages.

    :param chat_id:
    """
    subscriber_file = open(path + '/.chats', 'r')
    current_subscribers = subscriber_file.readlines()
    subscriber_file.close()
    new_chat_id = str(chat_id) + "\n"
    new_chat_ids = []
    # Add all users with a different id than the one who unsubscribed.
    for current_subscriber in current_subscribers:
        if not new_chat_id == current_subscriber:
            new_chat_ids.append(current_subscriber)
    chat_file = open(path + '/.chats', 'w')
    chat_file.write('')
    [chat_file.write(new_chat_id) for new_chat_id in new_chat_ids]
    chat_file.close()
