from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON, LEXICON_COMMANDS
from keyboard.inline_buttons import create_inline_kb, creat_btn_clear_status
from keyboard.regular_buttons import web_button
from fsm.fsm import FsmFindItem
from services.get_info_db import get_text_filters_from_db, get_brands, get_item, get_item_list
from services.base_logic import get_photo_obj


all_categories, all_names, all_brands = get_text_filters_from_db()
router: Router = Router()

# срабатывает на команду старт в дефолтном состоянии
@router.message(CommandStart(), StateFilter(default_state))
async def begin_bot(message: Message):
    await message.answer(LEXICON_COMMANDS['/start']['out'], 
                         reply_markup=web_button())


# срабатывает на команду старт в любом состоянии кроме дефолтного
@router.message(CommandStart(), ~StateFilter(default_state))
async def begin_bot(message: Message):
    await message.answer(LEXICON_COMMANDS['/start']['in'])

# срабатывает на команду хелп в любом состоянии
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(LEXICON_COMMANDS['/help']['in_out'])

# срабатывает на команду find

@router.message(Command('find'))
async def find_item(message: Message, state: FSMContext):
    сurent_state = await state.get_state()
    
    if сurent_state != None:
        await message.answer(LEXICON_COMMANDS['/find']['in'],
                         reply_markup=creat_btn_clear_status())
    else:
        # выводит инлайн клавиатуру для выбора категорий
        # переводит фсм в следующее состояние
        await message.answer(LEXICON_COMMANDS['/find']['out'], 
                            reply_markup=create_inline_kb(button_list=all_categories, cancel=True, back=False, width=1))
        await state.set_state(FsmFindItem.category_state)



# срабатывает на команду status в любом состоянии кроме дефолтного
@router.message(Command('status'))
async def find_item(message: Message, state: FSMContext):
    # в соответсвие с текущим статусом выводим сообщение
    сurent_state = await state.get_state()
    
    if сurent_state != None:
        choices = await state.get_data()
        await message.answer(LEXICON_COMMANDS['/status']['in'] + f'{choices}',
                            reply_markup=creat_btn_clear_status('Начать заново'))
    else:
        await message.answer(LEXICON_COMMANDS['/status']['out'])

# срабатывает на кнопку "Начать заново"
# в любых состояниях кроме дефолтного
@router.callback_query(~StateFilter(default_state), Text(text='clear_find'))
async def clear_data(callback: CallbackQuery, state: FSMContext):
    '''
    Очищает фсм контект, выводит об этом сообщение, устанавливает дефолтный статус
    '''
    await state.set_state(None)
    await state.clear()
    await callback.message.edit_text(text=LEXICON['cleared'])
    
    

# срабатывает при нажатии кнопки отмена
# в любых состояних кроме дефолтного
@router.callback_query(~StateFilter(default_state), Text(text='cancel'))
async def get_cancel(callback: CallbackQuery, state: FSMContext):
    '''
    Очищает контекст машины состояний
    Выводит об этом сообщение
    Сбрасывается к дефолтному состоянию
    '''

    await callback.message.edit_text(text=LEXICON['cancel'])
    await state.set_state(None)
    await state.clear()
    
    

# срабатывает на инлайн кнопку назад в любом режиме кроме дефолтного

@router.callback_query(~StateFilter(default_state), Text(text='back'))
async def get_back(callback: CallbackQuery, state: FSMContext):
    '''
    отправляет на 1 шаг назад для выбора категорий
    '''
    # определяем текущее состояние
    curent_state = await state.get_state()
    # если мы в ожидании получения бренда, то возвращаемся к выбору категорий
    if curent_state == FsmFindItem.brand_state:
        await callback.message.edit_text(LEXICON_COMMANDS['/find']['out'], 
                         reply_markup=create_inline_kb(button_list=all_categories, width=1, cancel=True, back=False))
        await state.set_state(FsmFindItem.category_state)
    
    # если мы в меню выбора имени товара, возвращаемся к выбору бренда
    elif curent_state == FsmFindItem.name_state:
        data = await state.get_data()
        category = data['category']
        brands = get_brands(category)
        await callback.message.edit_text(text=LEXICON['brand'],
                                        reply_markup=create_inline_kb(button_list=brands, width=3, cancel=True, back=True))
        await state.set_state(FsmFindItem.brand_state)

# срабатывает на нажатие одной из инлайн кнопок категорий

@router.callback_query(StateFilter(FsmFindItem.category_state), Text(text=all_categories))
async def get_category(callback: CallbackQuery, state: FSMContext):
    '''
    сохраняет выбор
    переводит машину в следующее состояние
    выводит сообщение и клавиатуру для следующего выбора
    '''
    # получаем выбранную категорию
    category = callback.data
    # отфильтровываем доступные бренды в этой категории
    brands: list = get_brands(category)

    await state.update_data(category=callback.data)
    await callback.message.edit_text(text=LEXICON['brand'],
                                    reply_markup=create_inline_kb(button_list=brands, width=3, cancel=True, back=True))
    await state.set_state(FsmFindItem.brand_state)
    


# срабатывает на нажатие кнопки с брендами
@router.callback_query(StateFilter(FsmFindItem.brand_state), Text(text=all_brands))
async def recieve_brand(callback: CallbackQuery, state: FSMContext):
    '''
    сохраняет выбор
    переводит машину в следующее состояние
    выводит сообщение и клавиатуру для следующего выбора
    '''
    data = await state.get_data()
    category = data['category']
    items: list[str] = get_item_list(category=category, brand=callback.data)

    await state.update_data(brand=callback.data)
    await callback.message.edit_text(text=LEXICON['show_items'],
                                  reply_markup=create_inline_kb(button_list=items, width=3, cancel=True, back=True))
    await state.set_state(FsmFindItem.name_state)

# срабатывает на нажатие кнопки с названием товара
@router.callback_query(StateFilter(FsmFindItem.name_state), Text(text=all_names))
async def recieve_item(callback: CallbackQuery, state: FSMContext):
    '''
    Обрабатывает сделанный выбор, отправляет сообщение с фото и краткой информацией о товаре
    Сбрасывает контекст ФСМ, переводит в дефолтное состояние
    '''
    await callback.answer()
    name = callback.data
    data = await state.get_data()
    brand, category = data['brand'], data['category']
    item: dict = get_item(category=category, brand=brand, name=name)
    await callback.message.answer_photo(photo=get_photo_obj(item),
                                        caption=f'Модель: {item["title"]}\n'
                                        f'Размеры: {item["size"]}\n'
                                        f'Цена: {item["price"]} $\n'
                                        f'Доступное количество: {item["count"]}',
                                        reply_markup = web_button()
                                        )
    await state.set_state(None)
    await state.clear()
    


# срабатывает на нажатие одной из инлайн кнопок категорий находясь в ином состоянии кроме ожидания категории
@router.callback_query(~StateFilter(FsmFindItem.category_state), Text(text=all_categories))
async def get_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['twice_choice_category'])

# срабатывает на нажатие одной из инлайн кнопок выбора бренда находясь в ином состоянии кроме ожидания бренда
@router.callback_query(~StateFilter(FsmFindItem.brand_state), Text(text=all_brands))
async def get_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['twice_choice_brand'])


# срабатывает на нажатие одной из инлайн кнопок товара находясь в ином состоянии кроме ожидания товара
@router.callback_query(~StateFilter(FsmFindItem.name_state), Text(text=all_names))
async def get_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['twice_choice_name'])

# срабатывает на все остальные сообщения
@router.message()
async def unknown_message(message: Message):
    await message.reply(text=LEXICON['unknown'])
