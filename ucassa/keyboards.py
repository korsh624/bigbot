from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def subscribekb():
    keyboard=InlineKeyboardMarkup()
    btn_subscribe=InlineKeyboardButton('Оплатить', callback_data='payment')
    btn_cancel=InlineKeyboardButton('Отмена', callback_data='cancel')
    keyboard.add(btn_subscribe, btn_cancel)
    return keyboard
def subcheck():
    keyboard=InlineKeyboardMarkup()
    btn_check=InlineKeyboardButton('Проверить подписку',callback_data='check')
    keyboard.add(btn_check)
    return keyboard