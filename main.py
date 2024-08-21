import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# Токен вашего Telegram-бота
API_TOKEN = '7505360526:AAHQF-wTEqoaBbg7xLwYvOHUaSe2_dV9o44'

# API-ключ OpenWeatherMap и базовый URL для запросов
WEATHER_API_KEY = ''
CITY = 'Voronezh'  # Укажите здесь город, для которого будет предоставляться прогноз погоды
WEATHER_BASE_URL = ''

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
        "/weather - Получить прогноз погоды"
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


# Хэндлер для обработки всех остальных сообщений
@dp.message()
async def echo(message: Message):
    await message.answer("Я не понимаю эту команду. Используйте /help для получения списка команд.")


async def main():
    # Пропускать обновления, которые бот получил, когда был офлайн
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск процесса обработки сообщений
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
