import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text

from os import getenv
from dotenv import load_dotenv

from main import get_data

load_dotenv()

token = getenv("token")

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Последние 5 новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Добро пожаловать, дорогой болельщик Зенита! Здесь ты можешь оперативно следить"
                         " за новостями футбольного клуба Зенит. Пользуйся мной с удовольствием!",
                         reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open("news.json", encoding="utf-8") as file:
        news_dict = json.load(file)

        if not news_dict:
            get_data()
            news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f"{hbold('Дата публикации: ', v['Дата публикации'])}\n" \
               f"{hlink(v['Заголовок'], v['Ссылка'])}"

        await message.answer(news)


@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_last_five_news(message: types.Message):
    with open("news.json", encoding="utf-8") as file:
        news_dict = json.load(file)

        if not news_dict:
            get_data()
            news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold('Дата публикации: ', v['Дата публикации'])}\n" \
               f"{hlink(v['Заголовок'], v['Ссылка'])}"

        await message.answer(news)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = get_data()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold('Дата публикации: ', v['Дата публикации'])}\n" \
                   f"{hlink(v['Заголовок'], v['Ссылка'])}"

            await message.answer(news)

    else:
        await message.answer("Пока нет свежих новостей...")


if __name__ == '__main__':
    executor.start_polling(dp)
