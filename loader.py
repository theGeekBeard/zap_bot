from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from data.config import DATABASE_URL, DATABASE_KEY
from database import Database

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = Database(DATABASE_URL, DATABASE_KEY)
