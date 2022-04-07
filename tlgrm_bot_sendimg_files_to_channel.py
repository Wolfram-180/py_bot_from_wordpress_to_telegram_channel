import logging
from aiogram import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewares import AccessMiddleware
import aiogram.utils.markdown as md
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ParseMode
import os

import secrets

logging.basicConfig(level=logging.INFO)

API_TOKEN = secrets.admin_bot_token

PROXY_URL = ''
PROXY_AUTH = ''

storage = MemoryStorage()

bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot, storage=storage)

restrict_access = False

if restrict_access:
    dp.middleware.setup(AccessMiddleware(secrets.admin_TG_ID))

cmnd_start = 'start'
cmnd_cancel = 'cancel'
cmnd_list_files_to_load = 'list'
cmnd_send_files_to_channel = 'send_to_channel'


@dp.message_handler(commands=[cmnd_start])
async def start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton(cmnd_list_files_to_load))
    markup.row(KeyboardButton(cmnd_cancel))
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Hello'),
            md.text('Your TG ID: {} \n'.format(message.chat.id)),
            md.text('Commands:'),
            md.text(cmnd_start),
            md.text(cmnd_list_files_to_load),
            md.text(cmnd_cancel),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )    


@dp.message_handler(commands=[cmnd_list_files_to_load])
async def list_files(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton(cmnd_send_files_to_channel))
    markup.row(KeyboardButton(cmnd_cancel))
    file_list = os.listdir(secrets.load_path)
    await bot.send_message(
        message.chat.id,
        md.text(file_list),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )   


@dp.message_handler(commands=[cmnd_send_files_to_channel])
async def send_files(message: types.Message):
    bot.send_message(message.chat.id, 'Implementation in process', parse_mode = 'Markdown')  


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)