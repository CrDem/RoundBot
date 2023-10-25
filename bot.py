from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

PROXY_URL = 'http://proxy.server:3128'
token_api = "6565587911:AAGG80wsIafXZdshqZXwkLuNWfXk735rmkk"
#bot = Bot(token=token_api, proxy=PROXY_URL)
bot = Bot(token=token_api)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

@dp.message_handler()
async def any_message(message: types.Message):
    await message.answer("Просто отправь мне видео! (до 20мб)")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
