from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ContentType
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text, CommandStart
import asyncio

from os import getenv
from dotenv import load_dotenv

from main import get_data

load_dotenv()

token = getenv("token")

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

user_id = getenv("user_id")


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup([
        [
            KeyboardButton(text="Свежие новости")
        ]
    ],
        resize_keyboard=True)

    await message.answer("Добро пожаловать, дорогой болельщик Зенита! Здесь ты можешь оперативно следить"
                         f" за новостями футбольного клуба Зенит. Пользуйся мной с удовольствием!",
                         reply_markup=keyboard)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    await message.answer("Ожидайте, извлекаю информацию о новостях...")

    fresh_news = get_data()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold('Дата публикации:', v['Дата публикации'])}\n" \
                   f"{hlink(v['Заголовок'], v['Ссылка'])}"

            await message.answer(news, disable_notification=True)

    else:
        await message.answer("Пока нет свежих новостей...")


@dp.message_handler(content_types=ContentType.ANY)
async def send_message(message: types.Message):
    await message.reply("И что мне с этим делать? "
                        "Чтобы взаимодействовать с ботом, используйте кнопку 'Свежие новости'. ")


async def get_fresh_news_period():
    while True:
        await asyncio.sleep(60)

        fresh_news = get_data()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold('Дата публикации:', v['Дата публикации'])}\n" \
                       f"{hlink(v['Заголовок'], v['Ссылка'])}"

                await bot.send_message(user_id, news, disable_notification=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(get_fresh_news_period())
    executor.start_polling(dp)
