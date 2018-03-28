# import discord # learn more: https://python.org/pypi/discord
from discord_hooks import Webhook
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
import logging
import os

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('PHONE_NUMBER')
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
telegram_chats = os.getenv(
    'TELEGRAM_CHATS', 'SharkSniper,CoinSniper,WallMonitor').split(',')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

client = TelegramClient(phone, api_id, api_hash,
                        update_workers=4, spawn_read_thread=False)
client.start()

chats = []
for chat in telegram_chats:
    if chat.isdigit():
        chat = int(chat)
    chats.append(chat)
print('Channels: ', chats)


@client.on(events.NewMessage(chats=chats, incoming=True))
def event_handler(event):
    msg_text = event.text  # event.raw_text
    import re
    url_reg = r'\((http[^)]+)\)'
    msg_text = re.sub(url_reg, r'(<\1>)', msg_text)
    msg = Webhook(discord_webhook_url, msg=msg_text)
    # print(event)
    print(event.input_sender, event.document, event.text)
    msg.post()


client.idle()
client.disconnect()

# Resources
# https://www.devdungeon.com/content/discord-webhook-tutorial-check-bitcoin-price-python
# https://www.devdungeon.com/content/make-discord-bot-python-part-2
# https://hackaday.com/2018/02/15/creating-a-discord-webhook-in-python/
# https://github.com/fritzr/discord-twitter-bot
# https://github.com/NxtStudios/DiscordHooks
# https://habrahabr.ru/post/322078/
# https://toster.ru/q/466436
# https://github.com/DevDungeon/ChattyCathy
# https://github.com/kyb3r/dhooks
# https://github.com/aubguillemette/discord2slack
# http://telethon.readthedocs.io/en/latest/extra/basic/entities.html
