from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def get_main_kb():
    main_keyboard=InlineKeyboardMarkup()
    btn1=InlineKeyboardButton('Файл 1', callback_data='file1')
    btn_cncl=InlineKeyboardButton('Отмена', callback_data='cancel')
    main_keyboard.add(btn1,btn_cncl)
    return main_keyboard

def get_help_kb():
    keyboard_help=InlineKeyboardMarkup()
    btn_help=InlineKeyboardButton('Помощь', callback_data='help')
    keyboard_help.add(btn_help)
    return keyboard_help