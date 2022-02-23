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
    start_buttons = ["Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Добро пожаловать, дорогой болельщик Зенита! Здесь ты можешь оперативно следить"
                         " за новостями футбольного клуба Зенит. Пользуйся мной с удовольствием!",
                         reply_markup=keyboard)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    await message.answer("Ожидайте, извлекаю информацию о новостях...")

    fresh_news = get_data()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold('Дата публикации:', v['Дата публикации'])}\n" \
                   f"{hlink(v['Заголовок'], v['Ссылка'])}"

            await message.answer(news)

    else:
        await message.answer("Пока нет свежих новостей...")


@dp.message_handler(content_types=["text"])
async def send_message(message: types.Message):
    await message.answer("Чего ты тут мне пишешь? У тебя же кнопки есть!")


if __name__ == '__main__':
    executor.start_polling(dp)
