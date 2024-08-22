import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from gtts import gTTS
import os
from aiogram.types import Message, FSInputFile
from googletrans import Translator

import random
# Токен вашего Telegram-бота
API_TOKEN = ''

# API-ключ OpenWeatherMap и базовый URL для запросов
WEATHER_API_KEY = ''
CITY = 'Voronezh'  # Укажите здесь город, для которого будет предоставляться прогноз погоды
WEATHER_BASE_URL = ''

translator = Translator()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)

# Инициализация диспетчера
dp = Dispatcher()


# Команда /start
@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Привет! Я ваш Telegram-бот. Используйте команду /help для получения списка доступных команд.")


# Команда /help
@dp.message(Command('help'))
async def send_help(message: Message):
    help_text = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить список команд\n"
        "/weather - Получить прогноз погоды\n"
        "/voice - Получить голосовое сообщение от бота\n"
        "Отправьте текст, и я переведу его на английский.\n"
        "Просто отправьте мне фото, и я сохраню его на диск."
    )
    await message.answer(help_text)


# Команда /weather
@dp.message(Command('weather'))
async def send_weather(message: Message):
    weather_url = f"{WEATHER_BASE_URL}?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(weather_url)

    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description'].capitalize()
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        weather_report = (
            f"Погода в городе {CITY}:\n"
            f"Описание: {weather_description}\n"
            f"Температура: {temperature}°C (ощущается как {feels_like}°C)\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
        await message.answer(weather_report)
    else:
        await message.answer("Не удалось получить данные о погоде. Попробуйте снова позже.")


@dp.message(F.photo)
async def handle_photo(message: Message):
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')

# Хэндлер для обработки всех остальных сообщений
@dp.message()
async def echo(message: Message):
    await message.answer("Я не понимаю эту команду. Используйте /help для получения списка команд.")

# @dp.message(Command('voice'))
# async def voice(message: Message):
#     voice = FSInputFile("sample.ogg")
#     await message.answer_voice(voice)
# @dp.message(Command('training'))
# async def training(message: Message):
#    training_list = [
#        "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
#        "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
#        "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
#    ]
#    rand_tr = random.choice(training_list)
#    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")
#
#    tts = gTTS(text=rand_tr, lang='ru')
#    tts.save('training.ogg')
#    audio = FSInputFile('sound2.ogg')
#    await bot.send_audio(message.chat.id, audio)
#    os.remove('training.ogg')
# @dp.message(Command('voice'))
# async def voice(message: Message):
#     voice = FSInputFile("sample.ogg")
#     await message.answer_voice(voice)

# Команда для отправки голосового сообщения
@dp.message(Command('voice'))
async def send_voice_message(message: Message):
    voice_path = f"{AUDIO_DIR}/voice_message.ogg"

    # Проверьте, существует ли заранее записанное голосовое сообщение
    if not os.path.exists(voice_path):
        await message.answer("привет.")
        return

    voice_file = FSInputFile(voice_path)
    await bot.send_voice(chat_id=message.chat.id, voice=voice_file, caption="Вот ваше голосовое сообщение!")


async def translate_to_english(message: Message):
    translated_text = translator.translate(message.text, dest='en').text
    await message.answer(f"Перевод на английский: {translated_text}")
async def main():
# Пропускать обновления, которые бот получил, когда был офлайн
    await bot.delete_webhook(drop_pending_updates=True)

# Запуск процесса обработки сообщений
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
