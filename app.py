# import discord # learn more: https://python.org/pypi/discord
from discord_hooks import Webhook
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
import logging
import os
import re
import json
import requests

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('PHONE_NUMBER')
#discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
#telegram_chats = os.getenv('TELEGRAM_CHATS', []).split(',')

# 1. base-cracks-binance
webhook_1 = 'https://discordapp.com/api/webhooks/433634416837787649/HY7kU6BfNql1FoIwdFxzIrRo9tqRpTw7IUkIToas_O2tqjyNMOJ60RJfaHYcP6SqnR5Y'
telegram_chats_1 = ('binance_scanner,1151625426,1119530640').split(',')

# 2. base-cracks-bittrex
webhook_2 = 'https://discordapp.com/api/webhooks/433634706572050453/gn0auB-1ssEuGSzqLtgCPd3EjHQPCbJX9bjnuNiY5yLdyBdGTwCdpqR-pBPQdhfHI9T5'
telegram_chats_2 = ('1158021569,1319829254').split(',')

# 3. base-cracks-hitbtc
webhook_3 = 'https://discordapp.com/api/webhooks/433634828982812683/hU1zXSqN_H12ZQrMmTOXxbopzKFWy7a5AnNsgpcEsM0TFqHl2w69gpnP583Krr9Gfphv'
telegram_chats_3 = ('hitbtc_scanner').split(',')

# 4. rapid-price-drops
webhook_4 = 'https://discordapp.com/api/webhooks/433634950948978688/qmaxro9KmodBST3x48zSJ-JHsnjFNiqgVBk2dRH8LgcgBLXbQbJV8RaqzJUKM1KUn27v'
telegram_chats_4 = ('rapid_trading_scanner').split(',')

# 5. crypto-news
webhook_5 = 'https://discordapp.com/api/webhooks/433635768272027678/atb098BoDjCkZCEeR1CqMpvoK-drfzrrsD7PbG1BbsZgiTBauhz-R3DX0-l1GAo35H_d'
telegram_chats_5 = ('biergodnews').split(',')

# 6. coin-delistings
webhook_6 = 'https://discordapp.com/api/webhooks/433636015060680705/MSQ6Aaq4IgiSzxQX2tHuwc-mvVqoVGUrt6f3EFc1UxwutEMOhFPw2SPaGmdFPOS68-fa'
telegram_chats_6 = ('BittrexDelistings').split(',')

# 7. bitmex-liquidations
webhook_7 = 'https://discordapp.com/api/webhooks/433636393269461002/xv87dI88mGvWDuQEV3PR0eY3wbJ70szy_NNDBAWGkpJZbT_HCI1SYBCiGz6Y3cykk9_n'
telegram_chats_7 = ('BitmexRekt').split(',')

# 8. QFL DayTraders (to Slack #daytrade)
webhook_8 = 'https://hooks.slack.com/services/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'
telegram_chats_8 = ('QFLDayTradersTest').split(',')

# 9. QFL DayTraders (to Discord #base-cracks-binance)
webhook_9 = 'https://discordapp.com/api/webhooks/433634416837787649/HY7kU6BfNql1FoIwdFxzIrRo9tqRpTw7IUkIToas_O2tqjyNMOJ60RJfaHYcP6SqnR5Y'
telegram_chats_9 = ('QFLDayTradersTest').split(',')

'''
# Xypher
webhook_1 = 'https://discordapp.com/api/webhooks/428831056280551424/Fqvd2z98trD_cBgXexosew18VSwPG7sb79Ugei2IbVIF6qdABolp2w-nX8HHD8XvT4Qe'
telegram_chats_1 = ('SharkSniper,CoinSniper,WallMonitor').split(',')

# Base Signals
webhook_2 = 'https://discordapp.com/api/webhooks/428831899037990922/L8esjfkS-oPw7oAhIE91G9EnOhzukC9oUyHR9QBhGYwe0egWpkLr_zueIZ4f9z2mokiQ'
telegram_chats_2 = (
    'binance_scanner,hitbtc_scanner,1151625426,1119530640').split(',')

# TA Signals
webhook_3 = 'https://discordapp.com/api/webhooks/428831478273671178/XQU0XyUCrq8_sbzJPyDdCUeqyta4NpPpZX84hSvpNjp7NBPbeVQUrc_ru_0mt8jEK2c7'
telegram_chats_3 = ('CocaKitty,cointrendz').split(',')

# News
webhook_4 = 'https://discordapp.com/api/webhooks/427820403788873738/Ccgp5nsq0TncjsNvZB36XNoIFAIYcqyphS1AEk4P8yN6zM3zpRf7Kno-tGVvMvRYUlS7'
telegram_chats_4 = ('www_Bitcoin_com,BitcoinBot').split(',')
'''

bindings = [
    {'webhook': webhook_1, 'telegram_chats': telegram_chats_1},
    {'webhook': webhook_2, 'telegram_chats': telegram_chats_2},
    {'webhook': webhook_3, 'telegram_chats': telegram_chats_3},
    {'webhook': webhook_4, 'telegram_chats': telegram_chats_4},
    {'webhook': webhook_5, 'telegram_chats': telegram_chats_5},
    {'webhook': webhook_6, 'telegram_chats': telegram_chats_6},
    {'webhook': webhook_7, 'telegram_chats': telegram_chats_7},
    {'webhook': webhook_8, 'telegram_chats': telegram_chats_8},
    {'webhook': webhook_9, 'telegram_chats': telegram_chats_9}
]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

client = TelegramClient('telegram', api_id, api_hash,
                        update_workers=4, spawn_read_thread=False)
client.start()


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
    telegram_chats = []
    for chat in bind['telegram_chats']:
        if chat.isdigit():
            chat = int(chat)
        telegram_chats.append(chat)
    webhook = bind['webhook']
    logger.info('Channels: %s  ➡️  Webhook: %s' % (telegram_chats, webhook))
    add_handler(telegram_chats, webhook)


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
# https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784
