from dotenv import load_dotenv
from discord_hooks import Webhook
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
import logging
import os
import re
import json
import requests

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('PHONE_NUMBER')
print(phone)

# 1. kings-of-binance
webhook_1 = os.getenv('DISCORD_WEBHOOK_1')
telegram_chats_1 = os.getenv('TELEGRAM_CHANNEL_1').split(',')

# 2. crypto-society
webhook_2 = os.getenv('DISCORD_WEBHOOK_2')
telegram_chats_2 = os.getenv('TELEGRAM_CHANNEL_2').split(',')

# 3. highest-crypto
webhook_3 = os.getenv('DISCORD_WEBHOOK_3')
telegram_chats_3 = os.getenv('TELEGRAM_CHANNEL_3').split(',')

# 4. whale-leaks
webhook_4 = os.getenv('DISCORD_WEBHOOK_4')
telegram_chats_4 = os.getenv('TELEGRAM_CHANNEL_4').split(',')

# 5. ???
webhook_5 = os.getenv('DISCORD_WEBHOOK_5')
telegram_chats_5 = os.getenv('TELEGRAM_CHANNEL_5').split(',')

# 6. ???
webhook_6 = os.getenv('DISCORD_WEBHOOK_6')
telegram_chats_6 = os.getenv('TELEGRAM_CHANNEL_6').split(',')

# 7. ???
webhook_7 = os.getenv('DISCORD_WEBHOOK_7')
telegram_chats_7 = os.getenv('TELEGRAM_CHANNEL_7').split(',')

# 8. ???
webhook_8 = os.getenv('DISCORD_WEBHOOK_8')
telegram_chats_8 = os.getenv('TELEGRAM_CHANNEL_8').split(',')


bindings = [
    {'webhook': webhook_1, 'telegram_chats': telegram_chats_1},
    {'webhook': webhook_2, 'telegram_chats': telegram_chats_2},
    {'webhook': webhook_3, 'telegram_chats': telegram_chats_3},
    {'webhook': webhook_4, 'telegram_chats': telegram_chats_4},
    {'webhook': webhook_5, 'telegram_chats': telegram_chats_5},
    {'webhook': webhook_6, 'telegram_chats': telegram_chats_6},
    {'webhook': webhook_7, 'telegram_chats': telegram_chats_7},
    {'webhook': webhook_8, 'telegram_chats': telegram_chats_8}
]


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

client = TelegramClient('telegram', api_id, api_hash,
                        update_workers=4, spawn_read_thread=False)
client.start(phone)


def add_handler(telegram_chats, webhook):
    @client.on(events.NewMessage(chats=telegram_chats, incoming=True))
    def event_handler(event):
        if "discordapp.com" in webhook:
            #post_to_discord(event, webhook)
            logger.info('Posting to Discord')
        elif "slack.com" in webhook:
            #post_to_slack(event, webhook)
            logger.info('Posting to Slack')


def post_to_discord(event, webhook):
    msg_text = event.text  # event.raw_text
    url_reg = r'(https?[:.]+[^\s\)]+)'
    msg_text = re.sub(url_reg, r'<\1>', msg_text)
    msg = Webhook(webhook, msg=msg_text)
    msg.post()
    #print(event.input_sender, event.document, event.text)
    logger.info('Delivered to webhook %s' % (webhook))


def post_to_slack(event, webhook):
    msg_text = event.text  # event.raw_text
    url_reg = r'(https?[:.]+[^\s\)]+)'
    msg_text = re.sub(url_reg, r'<\1>', msg_text)
    resp = requests.post(webhook, json={"text": msg_text, "mrkdwn": True}, headers={
                         'Content-Type': 'application/json'})
    logger.info('Delivered to webhook %s (response: %s)' %
                (webhook, resp.status_code))


for bind in bindings:
    if (bind['webhook'] == '') or (bind['telegram_chats'] == ['']):
        continue
    webhook = bind['webhook']
    telegram_chats = []
    for chat in bind['telegram_chats']:
        if chat.isdigit():
            chat = int(chat)
        telegram_chats.append(chat)
    logger.info('Channels: %s  ➡️  Webhook: %s' % (telegram_chats, webhook))
    add_handler(telegram_chats, webhook)


client.idle()
client.disconnect()
