from aiogram import Bot,Dispatcher,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
import logging
import config


logging.basicConfig(level=logging.INFO)


user_message='Пользователь'
admin_message='Админ'

if __name__=='__main__':
    executor.start_polling(dp,skip_updates=False)