import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN,TOKEN_KINO,ADMINS,url
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


main_menu=InlineKeyboardMarkup()
btn_search=InlineKeyboardButton('Случайный фильм', callback_data='random')
btn_reviews=InlineKeyboardButton('Отзывы',callback_data='reviews')
main_menu.add(btn_search,btn_reviews)


random_film_kb=InlineKeyboardMarkup()
btn_new_film=InlineKeyboardButton('Другой фильм',callback_data='random')
random_film_kb.add(btn_new_film)


@dp.message_handler(commands=['start'])
async def get_menu(message:types.Message):
   if (str(message.chat.id) in ADMINS):
      await message.answer('Нажмите на кнопку для получения фильма',reply_markup=main_menu)

headers={'accept': 'application/json', 'X-API-KEY': TOKEN_KINO}


@dp.callback_query_handler(text='random')
async def get_random(callback:types.CallbackQuery):
   r=requests.get(url+ 'v1/movie/random', headers=headers)
   print(r)
   if r.status_code==200:
      title=r.json()['name']
      description=r.json()['description']
      year=r.json()['year']
      rating=r.json()['rating']['kp']
      await bot.answer_callback_query(callback.id)
      await bot.send_message(callback.from_user.id,f'Фильм {title}')
      await bot.send_message(callback.from_user.id, f'Описание {description}')
      await bot.send_message(callback.from_user.id, f'Год выпуска {year}')
      await bot.send_message(callback.from_user.id, f'Рейтинг {rating}',reply_markup=random_film_kb)


@dp.callback_query_handler(text='reviews')
async def get_reviews(callback:types.CallbackQuery):
   r=requests.get(url+'v1/review?page=1&limit=10', headers=headers)
   if r.status_code==200:

      r=r.json()['docs']
      for rw in r:
         id = rw['movieId']
         r_film = requests.get(url + 'v1.3/movie/' + str(id), headers=headers)
         title_film = r_film.json()['name']
         if title_film:
            await bot.send_message(callback.from_user.id, f'Фильм: {title_film}')
         title=rw['title']
         review=rw['review']
         author=rw['author']
         await bot.answer_callback_query(callback.id)
         await bot.send_message(callback.from_user.id, f'Заголовок: {title}')
         await bot.send_message(callback.from_user.id, f'Обзор: {review}')
         await bot.send_message(callback.from_user.id, f'Автор: {author}')


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
