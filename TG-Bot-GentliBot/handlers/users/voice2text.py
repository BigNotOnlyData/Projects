import subprocess

from aiogram import types

from loader import dp, bot
from utils.voice import text_from_audio
from data.config import VOICE_FILE_PATH, AUDIO_FILE_PATH


@dp.message_handler(content_types=types.ContentTypes.VOICE)
async def voice2text(message: types.Message):
    """
    Принимает голосовые сообщения (.ogg), конвертирует с помощью программы ffmeg в формат (.wav)
    и переводит аудио в текст
    """
    try:
        voice_info = await bot.get_file(message.voice.file_id)
        await bot.download_file(voice_info.file_path, VOICE_FILE_PATH)
        subprocess.run(['ffmpeg', '-i', VOICE_FILE_PATH, AUDIO_FILE_PATH, '-y'])
        text = text_from_audio(str(AUDIO_FILE_PATH))
        await message.reply(text)
    except Exception:
        print("Ошибка в функции voice2text")


