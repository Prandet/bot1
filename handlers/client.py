from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
import random
import re
import requests
from aiogram.types import ReplyKeyboardRemove

async def commands_start(message: types.Message):
    await message.answer('Приятно познакомиться, я бот созданный для общения с тобой:)', reply_markup=kb_client)

async def romeo_talks_command(message: types.Message):
    await message.answer('12:00-22:00. В любой день недели')

async def how_are_you_command(message: types.Message):
    await message.answer('Отлично, спасибо за ваш интерес!')

async def bot_command(message: types.Message):
    await message.answer('Чем могу помочь?')

predefined_responses = {
    "как дела": "Отлично, спасибо за ваш интерес!",
    "что ты умеешь": "Я могу помочь вам узнать время работы и ответить на вопросы. Просто спросите!",
    "слава україні": "Героям слава!",
    # Добавьте другие вопросы и ответы по необходимости
}

def get_weather(city):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 49.75,
        "longitude": 15,
        "hourly": "temperature_2m",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "hourly" in data and "temperature_2m" in data["hourly"]:
        temperature = data["hourly"]["temperature_2m"][0]
        return f"Текущая температура в {city.capitalize()}: {temperature}°C"
    else:
        return f"Извините, не удалось получить данные о погоде для {city.capitalize()}"

async def generate_general_response(message: types.Message):
    user_input = message.text

    response_templates = [
        f"Интересно, расскажите мне больше о {user_input}.",
        f"Я понял. Как вы чувствуете себя, говоря о {user_input}?",
        f"Понятно. Почему именно {user_input}? Расскажите подробнее.",
        f"Увлекательно! Какие ещё мысли у вас есть по поводу {user_input}?",
        f"Слушаю вас. Что вызвало ваш интерес к {user_input}?",
    ]
    response = random.choice(response_templates)
    await message.answer(response)

async def process_text_message(message: types.Message):
    user_input = message.text.lower()

    response = predefined_responses.get(user_input)
    if response:
        await message.answer(response)
    elif re.search(r"погода", user_input):
        city_match = re.search(r"погода\s+(.+)", user_input)
        if city_match:
            city = city_match.group(1)
            weather_response = get_weather(city)
            await message.answer(weather_response)
        else:
            await message.answer("Чтобы узнать погоду, напишите 'погода ГОРОД'")
    else:
        await generate_general_response(message)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(romeo_talks_command, commands=['Время_работы'])
    dp.register_message_handler(how_are_you_command, commands=['Как_дела'])
    dp.register_message_handler(bot_command, commands=['Бот'])
    dp.register_message_handler(process_text_message)
