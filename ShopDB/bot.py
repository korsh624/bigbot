from aiogram import executor
import logging

logging.basicConfig(level=logging.INFO)


user_message='Пользователь'
admin_message='Админ'

if __name__=='__main__':
    executor.start_polling(dp,skip_updates=False)