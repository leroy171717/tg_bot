import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from dotenv import find_dotenv, load_dotenv
from aiogram.types import BotCommandScopeAllPrivateChats
from bot_cmds_list import private
load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


#btnMenu = KeyboardButton(text='Меню столовой на сегодня')
#btnUser = KeyboardButton(text='Собрать меню')
#mainMenu = ReplyKeyboardMarkup.add(btnMenu, btnUser)
#mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
#btnInfo = KeyboardButton('Информация')
#dp.include_router(user_private_router)

#btnMenu = KeyboardButton(text="Меню столовой на сегодня")
#btnUser = KeyboardButton(text='Собрать меню')
#mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnMenu, btnUser)

#btnInfo = KeyboardButton(text='Информация')

#user_private_router = Router()

@dp.message(Command('menu'))
async def start_cmd(message: types.Message):
    await message.answer("Меню:")

@dp.message(Command('about'))
async def start_cmd(message: types.Message):
    await message.answer("О нас:")

@dp.message(Command('info'))
async def start_cmd(message: types.Message):
    await message.answer("Информация:")

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет!")


async def main() -> None:
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

asyncio.run(main())