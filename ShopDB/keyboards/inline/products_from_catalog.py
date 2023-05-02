from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

product_cb=CallbackData('product','id','action')
def product_markup(idx='',price=0):
    global product_cb
    marckup=InlineKeyboardMarkup()
    marckup.add(InlineKeyboardButton(f'Добавить в корзину - {price}Р', callback_data=product_cb.new(id=idx,action='add')))
    return marckup