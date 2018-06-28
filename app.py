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

# mappings between telegram sources and webhook destinations (discord/slack)
bindings = [
    {'webhook': os.getenv('DISCORD_WEBHOOK_1'),
     'telegram_chats': os.getenv('TELEGRAM_CHANNEL_1').split(',')},
    {'webhook': os.getenv('DISCORD_WEBHOOK_2'),
     'telegram_chats': os.getenv('TELEGRAM_CHANNEL_2').split(',')},
    {'webhook': os.getenv('DISCORD_WEBHOOK_3'),
     'telegram_chats': os.getenv('TELEGRAM_CHANNEL_3').split(',')},
    {'webhook': os.getenv('DISCORD_WEBHOOK_4'),
     'telegram_chats': os.getenv('TELEGRAM_CHANNEL_4').split(',')},
    {'webhook': os.getenv('DISCORD_WEBHOOK_5'),
     'telegram_chats': os.getenv('TELEGRAM_CHANNEL_5').split(',')},
    {'webhook': os.getenv('DISCORD_WEBHOOK_6'),
     'telegram_chats': os.getenv('TELEGRAM_CHANNEL_6').split(',')},
    {'webhook': os.getenv('DISCORD_WEBHOOK_7'),
     'telegram_chats': os.getenv('TELEGRAM_CHANNEL_7').split(',')},
    {'webhook': os.getenv('DISCORD_WEBHOOK_8'),
     'telegram_chats': os.getenv('TELEGRAM_CHANNEL_8').split(',')},
    {'webhook': os.getenv('DISCORD_WEBHOOK_9'),
     'telegram_chats': os.getenv('TELEGRAM_CHANNEL_9').split(',')},
    {'webhook': os.getenv('DISCORD_WEBHOOK_10'),
     'telegram_chats': os.getenv('TELEGRAM_CHANNEL_10').split(',')}
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
            post_to_discord(event, webhook)
        elif "slack.com" in webhook:
            post_to_slack(event, webhook)


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
