# Modules

from aiogram import Dispatcher, Bot
import config
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlighter import MongoDB

# Log

"""Logging and States"""

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

# Default Variebles

"""Common variables for aiogram and class with reference to the base"""

mongo = MongoDB(
    "mongodb+srv://Hellen:fbnz32iZA1ho49iy@cluster0.aqrqr.mongodb.net/yuhu-bot?retryWrites=true&w=majority"
)
bot = Bot(config.token, parse_mode="html")
db = Dispatcher(bot, storage=storage)
