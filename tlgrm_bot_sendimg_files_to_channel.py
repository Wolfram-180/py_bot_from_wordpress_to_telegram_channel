import logging
from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewares import AccessMiddleware
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
    ACCESS_ID = ''
    dp.middleware.setup(AccessMiddleware(ACCESS_ID))



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)