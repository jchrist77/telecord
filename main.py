#import discord # learn more: https://python.org/pypi/discord
from discord_hooks import Webhook
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
import logging
import os

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('PHONE_NUMBER')
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
telegram_chats = (
    'SharkSniper',
    'CoinSniper',
    'WallMonitor',
    'binance_scanner',
    'CocaKitty',
    1151625426,	# Hodloo Binance 5%
    1119530640,	# Hodloo Binance 10%
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

client = TelegramClient(phone, api_id, api_hash, update_workers=4, spawn_read_thread=False)
client.start()

@client.on(events.NewMessage(chats=telegram_chats, incoming=True))
def event_handler(event):
    msg = Webhook(discord_webhook_url, msg=event.raw_text)
    msg.post()

client.idle()
client.disconnect()

### Resources
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
