import os
import telepot
from dotenv import load_dotenv

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telepot.Bot(token)
me = bot.getMe()
print(me)

from pprint import pprint
response = bot.getUpdates()
pprint(response)
