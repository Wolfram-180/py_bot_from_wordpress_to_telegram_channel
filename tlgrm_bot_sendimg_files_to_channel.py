import logging
from time import sleep
from tkinter import NO
from aiogram import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewares import AccessMiddleware
import aiogram.utils.markdown as md
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ParseMode
import os

import environment_params

logging.basicConfig(filename='botlog.log', encoding='utf-8', level=logging.INFO)

API_TOKEN = environment_params.admin_bot_token

PROXY_URL = ''
PROXY_AUTH = ''

storage = MemoryStorage()

bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot, storage=storage)

restrict_access = True

if restrict_access:
    dp.middleware.setup(AccessMiddleware(environment_params.admin_TG_ID))

cmnd_start = 'start'
cmnd_cancel = 'cancel'
cmnd_list_files_to_load_and_than_send = 'list'
cmnd_send_files_to_channel = 'send_to_channel'

async def logandmess(str, chatid=0):
    logging.info(str)
    if chatid > 0:
        await bot.send_message(chatid, str) 


@dp.message_handler(commands=[cmnd_start])
async def start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton('/'+cmnd_start))
    markup.row(KeyboardButton('/'+cmnd_list_files_to_load_and_than_send))
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Hello'),
            md.text('Your TG ID: {} \n'.format(message.chat.id)),
            md.text('Commands:'),
            md.text(cmnd_start),
            md.text(cmnd_list_files_to_load_and_than_send),
            #md.text(cmnd_cancel),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )    


@dp.message_handler(commands=[cmnd_list_files_to_load_and_than_send])
async def list_files(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton('/'+cmnd_send_files_to_channel))
    markup.row(KeyboardButton('/'+cmnd_start))
    file_list = os.listdir(environment_params.load_path)
    await bot.send_message(
        message.chat.id,
        md.text(file_list),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )   


@dp.message_handler(commands=[cmnd_send_files_to_channel])
async def send_files(message: types.Message):
    start_file = environment_params.start_file

    await logandmess('Sending started from file: ' + start_file, message.chat.id)

    file_list = os.listdir(environment_params.load_path)

    for fl in file_list:
        currfilepos = file_list.index(fl)
        startfilepos = file_list.index(start_file)

        if currfilepos < startfilepos:
            continue        

        file_name, file_extension = os.path.splitext(fl)
        full_path_to_send = environment_params.load_path+fl
        if file_extension == '.gif':
            await bot.send_animation(chat_id=environment_params.chnl_ID, 
                animation=open(full_path_to_send, 'rb'))
        elif ((file_extension == '.mp4') or (file_extension == '.webm')):
            await bot.send_video(chat_id=environment_params.chnl_ID, 
                video=open(full_path_to_send, 'rb'))
        elif ((file_extension == '.jpg') 
            or (file_extension == '.jpeg')
            or (file_extension == '.png')):
            await bot.send_photo(chat_id=environment_params.chnl_ID, 
                photo=open(full_path_to_send, 'rb'))                
        else:
            await bot.send_document(chat_id=environment_params.chnl_ID, 
                document=open(full_path_to_send, 'rb'))

        await logandmess('Sent: ' + full_path_to_send, message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)