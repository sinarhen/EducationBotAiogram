from config import API_TOKEN
from aiogram import bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = bot.Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

