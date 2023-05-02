from aiogram import Bot,Dispatcher,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
from db import DatabaseManager
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage=MemoryStorage()
dp=Dispatcher(bot,storage=storage)
db=DatabaseManager('database.keyboards')