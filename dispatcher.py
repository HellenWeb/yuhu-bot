# Modules

from aiogram import Dispatcher, Bot
import config
import os
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlighter import MongoDB

# Log

"""Logging and States"""

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

# Default Variebles

"""Common variables for aiogram and class with reference to the base"""

mongo = MongoDB(os.getenv("MONGO_URI"))
bot = Bot(os.getenv("BOT_TOKEN"), parse_mode="html")
db = Dispatcher(bot, storage=storage)
