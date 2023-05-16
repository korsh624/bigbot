import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from config import BOT_TOKEN, SUPERUSER_IDS, Y_TOKEN
from keyboards import subscribekb, subcheck
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

subscribers = []
admins=SUPERUSER_IDS

@dp.message_handler(commands=['start'])
async def start_message(message:types.Message):
   id=str(message.from_user.id)
   if id in subscribers or id in admins:
      username=message.from_user.username
      await message.answer(f'Добро пожаловать {username}')
   else:
      await message.answer('Для начала работы вам нужно подписаться',reply_markup=subscribekb())

@dp.callback_query_handler(text='cancel')
async def push_cancel(callback: types.CallbackQuery):
   await callback.answer()
   await callback.message.answer('Вы отказались от подписки, \n Дальнейшая работа с ботом доступна только подпищикам')

@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
   await message.answer('Вы находитесь в информационном боте\n'
                        'Для взаимодействия с ботом необходима подписка\n'
                        'Если вы оформили подписку и она не активна напишите'
                        'пожалуйста администраторам @korsh624', reply_markup=subcheck())

@dp.callback_query_handler(text='check')
async def check_sub(callback: types.CallbackQuery):
    await callback.answer()
    id=str(callback.from_user.id)
    if id in admins:
        await callback.message.answer('Вы являетесь администратором')
    elif id in subscribers:
        await callback.message.answer('Подписка активирована')
    else:
        await callback.message.answer('Подписка не активна',reply_markup=subscribekb())

@dp.callback_query_handler(text='payment')
async def payment(callback:types.CallbackQuery):
    await bot.send_invoice(chat_id=callback.from_user.id, title='Подписка', description='Подписка на бота',
                           payload='payment', provider_token=Y_TOKEN, currency='RUB', start_parameter='test_bot',
                           prices=[{'label': 'Руб', 'amount': 10000}])

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_ckeckout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_ckeckout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message:types.Message):
    if message.successful_payment.invoice_payload=='payment':
        await bot.send_message(message.from_user.id,'Вы подписались')
        subscribers.append(str(message.from_user.id))


if __name__ == "__main__":
   executor.start_polling(dp, skip_updates=True)
