from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from database.requests import get_categories, get_category_item, get_days


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

async def days():
    all_days = await get_days()
    keyboard = InlineKeyboardBuilder()
    for day in all_days:
        keyboard.add(InlineKeyboardButton(text=day.name, callback_data=f"day_{day.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def items(category_id, day_id):
    all_items = await get_category_item(category_id, day_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()