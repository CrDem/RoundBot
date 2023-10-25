from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from editor import video_to_video_note
from os import remove

PROXY_URL = 'http://proxy.server:3128'
token_api = "6565587911:AAGG80wsIafXZdshqZXwkLuNWfXk735rmkk"
#bot = Bot(token=token_api, proxy=PROXY_URL)
bot = Bot(token=token_api)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

@dp.message_handler(content_types=['video'])
async def download_video(message: types.Message):
    try:
        file_id = message.video.file_id
        file = await bot.get_file(file_id)
        path = f"media/{file.file_unique_id}.mp4"
        await bot.download_file(file.file_path, path)
    except:
        await message.answer("Не удалось загрузить видео :(")
    else:
        await message.reply("Получили! Обрабатываем...")
        await send_video(message, file.file_unique_id)
@dp.message_handler()
async def any_message(message: types.Message):
    await message.answer("Просто отправь мне видео! (до 20мб)")


async def send_video(message, videoId):
    path = f"media/{videoId}.mp4"
    newPath = f"media/result{videoId}.mp4"
    if (video_to_video_note(path, newPath)):
        await message.answer_video_note(open(newPath, "rb"))
        if (video_to_video_note(path, newPath) == 'toolong'):
            await message.answer("Длительность видео больше минуты :(")
        else:
            await message.answer(
                "Для того, чтобы пересланное сообщение не было видно, при пересылке нажми на значок стрелки и выбери *скрыть имя отправителя*")
        # remove_files(path, newPath)


def remove_files(path, newPath):
    remove(path)
    remove(newPath)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
