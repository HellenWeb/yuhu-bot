
# Modules

from aiogram import Dispatcher, Bot
import config
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlighter import SQLighter

# Log

storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)

# Default Variebles

bot = Bot(config.token, parse_mode="html")
db = Dispatcher(bot, storage=storage)
dp = SQLighter('db.db')