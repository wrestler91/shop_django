from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# from ...models import Item, Category

# item_brands: list[Item] = [item.brand for item in Item.objects.all()]
# categories: list[Category] = [categ.name for categ in Category.objects.all()]

# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(width: int, button_list: list, cancel: bool = False, back: bool = False) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    
    for button in button_list:
        buttons.append(InlineKeyboardButton(text=button, callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    if cancel:
        cancel_btn = InlineKeyboardButton(text='\u274C Отмена', callback_data='cancel')
        kb_builder.row(cancel_btn, width=1)
    if back:
        back_btn = InlineKeyboardButton(text='Назад', callback_data='back')
        kb_builder.add(back_btn)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def creat_btn_clear_status(text: str = 'Начать сначала'):
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    button_clear: InlineKeyboardButton = InlineKeyboardButton(text=text, callback_data='clear_find')
    kb_builder.row(button_clear)

    return kb_builder.as_markup()