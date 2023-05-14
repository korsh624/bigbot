import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
   executor.start_polling(dp, skip_updates=True)
