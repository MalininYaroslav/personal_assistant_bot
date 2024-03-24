import os
import logging
import pytz

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


class BotConfig:
    def __init__(self, token: str):
        self._token = token
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.tz = pytz.timezone('Europe/Moscow')


logging.basicConfig(level=logging.DEBUG)
load_dotenv()
BOT_TOKEN = os.getenv('API_TOKEN')
config = BotConfig(BOT_TOKEN)
