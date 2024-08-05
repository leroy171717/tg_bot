from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging
import keyboards as kb
import database.requests as rq

router = Router()

class FSM(StatesGroup):
    day_id = State()
    category_id = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, это меню столовой!', reply_markup=kb.main)


@router.message(F.text == 'Меню')
async def menu(message: Message):
    await message.answer('Выберите день недели', reply_markup=await kb.days())

@router.callback_query(F.data.startswith('day_'))
async def days(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали день')
    await state.update_data(day_id=int(callback.data.split('_')[1]))
    await callback.message.answer('Выберите категорию',
                                  reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали категорию')
    data = await state.get_data()
    day_id = data.get('day_id')
    await state.update_data(category_id=int(callback.data.split('_')[1]))
    await callback.message.answer('Выберите блюдо по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1], day_id))

@router.callback_query(F.data.startswith('item_'))
async def items(callback: CallbackQuery):
    item_id = callback.data.split('_')[1]
    try:
        item_data = await rq.get_item(item_id)
        file_path = f"{item_data.image}"  # Ensure this contains the correct file path

        # Check if the file path is valid
        if not file_path:
            raise FileNotFoundError("Image file path is empty.")

        # Ensure the file path exists
        print(file_path)
        photo = FSInputFile(file_path)  # Correct w\\ay to instantiate InputFile with a file path
        await callback.answer('Вы выбрали товар')
        await callback.message.answer_photo(photo=photo, caption=f'Название: {item_data.name}\nЦена: {item_data.price} Р')
    except FileNotFoundError:
        #logger.error(f'File not found: {file_path}')
        await callback.answer('Ошибка: файл изображения не найден.')
        await callback.message.answer(f'Изображение для этого товара не найдено.\n '
                                      f'{item_data.name}\nЦена: {item_data.price} Р')
    except Exception as e:
        #logger.error(f'Unexpected error: {str(e)}')
        await callback.answer(f'Ошибка: {str(e)}')
        await callback.message.answer(f'Изображение для этого товара не найдено.\n '
                                      f'{item_data.name}\nЦена: {item_data.price} Р')

@router.callback_query(F.data == 'to_main')
async def items(callback: CallbackQuery):
    await callback.answer('Главное')
    await callback.message.answer('Вы вернулись в главное меню', reply_markup=kb.main)

@router.message(F.text == 'На главную')
async def menu(message: Message):
    await message.answer('Вы вернулись в главное меню', reply_markup=kb.main)