from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from configs.configs import SITE_URL

def web_button()->ReplyKeyboardMarkup:
    button: KeyboardButton = KeyboardButton(text='Перейти на сайт', web_app=WebAppInfo(url=SITE_URL))
    kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True, one_time_keyboard=True)
    return kb