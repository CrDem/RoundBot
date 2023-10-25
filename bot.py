#version 1.3
import os.path

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from editor import video_to_video_note, DurationCrop
from os import remove

PROXY_URL = 'http://proxy.server:3128'
token_api = '6565587911:AAGG80wsIafXZdshqZXwkLuNWfXk735rmkk'
bot = Bot(token=token_api, proxy=PROXY_URL)
#bot = Bot(token=token_api)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


class CropInf(StatesGroup):
    start = State()
    duration = State()


@dp.message_handler(content_types=['video'])
async def download_video(message: types.Message, state):
    path = f"media/{message.video.file_unique_id}.mp4"
    if os.path.exists(path):
        await message.reply("Получили! Обрабатываем...")
        async with state.proxy() as data:
            data['video_id'] = message.video.file_unique_id
            data['video_duration'] = message.video.duration
        await send_video(message, message.video.file_unique_id)
        return True
    try:
        file = await bot.get_file(message.video.file_id)
        await bot.download_file(file.file_path, path)
    except:
        await message.answer("Не удалось загрузить видео :(")
    else:
        await message.reply("Получили! Обрабатываем...")
        async with state.proxy() as data:
            data['video_id'] = message.video.file_unique_id
            data['video_duration'] = message.video.duration
        await send_video(message, message.video.file_unique_id)


@dp.message_handler()
async def any_message(message: types.Message):
    await message.answer("Просто отправь мне видео! (до 20мб)")


@dp.message_handler(state=CropInf.start, content_types=['text'])
async def startCrop_message(message, state):
    async with state.proxy() as data:
        duration = data['video_duration']
    try:
        start = float(message.text)
    except:
        await message.answer("Неверный формат ввода. Введите число")
    else:
        if start < duration:
            async with state.proxy() as data:
                data['cropStart'] = message.text
            await CropInf.next()
            await message.answer("Сколько видео будет длиться?")
        else:
            await message.answer("Время начала больше длительности видео")


@dp.message_handler(state=CropInf.duration)
async def durationCrop_message(message, state):
    async with state.proxy() as data:
        data['cropDuration'] = message.text
        path = f"media/{data['video_id']}.mp4"
        croppedPath = f"media/cropped{data['video_id']}.mp4"
        newPath = f"media/result{data['video_id']}.mp4"
        try:
            newDuration = float(message.text)
        except:
            await message.answer("Неверный формат ввода. Введите число")
        else:
            if int(data['video_duration']) - float(data['cropStart']) < newDuration:
                await message.answer("Длительность превышает допустимую")
            else:
                if (DurationCrop(path, croppedPath, data['cropStart'], data['cropDuration'])):
                    if (video_to_video_note(croppedPath, newPath)):
                        await message.answer_video_note(open(newPath, "rb"))
                        await message.answer(
                            "Для того, чтобы пересланное сообщение не было видно, при пересылке нажми на значок стрелки и выбери *скрыть имя отправителя*")
                        remove(path)
                        remove(croppedPath)
                        remove(newPath)
                        await state.finish()



async def send_video(message, videoId):
    path = f"media/{videoId}.mp4"
    newPath = f"media/result{videoId}.mp4"
    if (video_to_video_note(path, newPath)):
        if (video_to_video_note(path, newPath) == 'toolong'):
            await message.answer("Слишком большая длительность. С какой секунды обрезать видео?")
            await CropInf.start.set()
        else:
            await message.answer_video_note(open(newPath, "rb"))
            await message.answer("Для того, чтобы пересланное сообщение не было видно, при пересылке нажми на значок стрелки и выбери *скрыть имя отправителя*")
            remove(Path)
            remove(newPath)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
