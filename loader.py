import psycopg2
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from data import config
from data.config import DATABASE, USER, PASSWORD, HOST
from database import Database

from googletrans import Translator

tr = Translator()

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

con = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)
db = Database(con)
