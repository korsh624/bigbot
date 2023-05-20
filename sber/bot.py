import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType

storage=MemoryStorage()
from config import BOT_TOKEN, SUPERUSER_IDS, SBER_TOKEN
from keyboards import get_main_kb, get_help_kb
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
class Help(StatesGroup):
   waiting_message=State()

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
   await message.answer(f'Здравствуйте, {message.from_user.username}!')
   await message.answer('Для покупки выберете необходимый вариант ниже',reply_markup=get_main_kb())

@dp.message_handler(commands=['help'])
async def start(message:types.Message):
   await message.answer(f'Выберете необходимое дйствие',reply_markup=get_help_kb())

@dp.callback_query_handler(text='cancel')
async def cancel(callback:types.CallbackQuery):
   await bot.delete_message(callback.from_user.id,callback.message.message_id)

@dp.callback_query_handler(text='help')
async def help(callback:types.CallbackQuery, state:FSMContext):
   await callback.answer()
   await callback.message.answer('Опишите вашу проблему')
   await state.set_state(Help.waiting_message.state)

@dp.message_handler(state=Help.waiting_message)
async def send_msg(message: types.Message, state: FSMContext):
   text=message.text
   user=message.from_user.username
   await bot.send_message(SUPERUSER_IDS[0],f'Вам сообщение от {user}\n {text}')
   await state.finish()

@dp.callback_query_handler(text='file1')
async def payment(callback: types.CallbackQuery):
   await bot.send_invoice(chat_id=callback.from_user.id, title='Покупка', description='Покупка файла 1',
                          payload='payment', provider_token=SBER_TOKEN, currency='RUB', start_parameter='test_bot',
                          prices=[{'label': 'Руб', 'amount': 10000}])


@dp.pre_checkout_query_handler()
async def process_pre_check(pre_check:types.PreCheckoutQuery):
   await bot.answer_pre_checkout_query(pre_check.id,ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message:types.Message):
   if message.successful_payment.invoice_payload=='payment':
      await bot.send_message(message.from_user.id,'Вы купили файл')
      await message.reply_document(open('file1.txt','rb'))

if __name__ == "__main__":
   executor.start_polling(dp, skip_updates=True)
