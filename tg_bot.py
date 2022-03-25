import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ContentType
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text, CommandStart, CommandHelp
import asyncio

from os import getenv
from dotenv import load_dotenv

from main import get_data

load_dotenv()

token = getenv("token")
user_id = getenv("user_id")

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

auto_mode = False


async def get_fresh_news_period():
    while True:
        if auto_mode:
            await asyncio.sleep(600)

            fresh_news = get_data()

            if len(fresh_news) >= 1:
                for k, v in sorted(fresh_news.items()):
                    news = f"{hbold('Дата публикации:', v['Дата публикации'])}\n" \
                           f"{hlink(v['Заголовок'], v['Ссылка'])}"

                    await bot.send_message(user_id, news, disable_notification=True)
        else:
            break


async def current_keyboard(is_auto_mode):
    with open("news.json", encoding="utf-8") as file:
        all_news = json.load(file)

    if len(all_news) != 0:
        if is_auto_mode:
            auto_mode_button = "Отключить авто-режим"
        else:
            auto_mode_button = "Включить авто-режим"

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

        buttons_1 = ["Последние 10 новостей", "Свежие новости"]
        buttons_2 = [auto_mode_button]

        keyboard.add(*buttons_1)
        keyboard.add(*buttons_2)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

        button = ["Последние 10 новостей"]

        keyboard.add(*button)

    return keyboard


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    keyboard = await current_keyboard(auto_mode)

    await message.answer("Добро пожаловать, дорогой болельщик Зенита! Здесь ты можешь оперативно следить"
                         f" за новостями футбольного клуба Зенит. Пользуйся мной с удовольствием! "
                         f"Кстати, если ты хочешь ознакомиться со справкой, воспользуйся командой /help",
                         reply_markup=keyboard)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer(f"{hbold('СПРВКА')}\n"
                         f"При первом запуске бота будет доступна {hbold('одна кнопка')}: 'Последние 10 новостей'.\n"
                         f"Нажав на неё, вы получите 10 последних новостей, а также появятся {hbold('2 новые кнопки')}: "
                         "'Включить/выключить авто-режим' и 'Свежие новости'.\n"
                         f"{hbold('Свежие новости')} покажет все свежие новости, которые бот еще не показывал.\n"
                         f"{hbold('Включить/выключить авто-режим')} - функция, позволяющая автоматически проверять "
                         "вышедшие новости раз в 10 минут. Вы также можете отключить эту функцию.")


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


@dp.message_handler(Text(equals="Включить авто-режим"))
async def enable_auto_mode(message: types.Message):
    global auto_mode
    auto_mode = True

    keyboard = await current_keyboard(auto_mode)

    loop = asyncio.get_event_loop()
    loop.create_task(get_fresh_news_period())

    await message.answer("Авто-режим включен", reply_markup=keyboard)


@dp.message_handler(Text(equals="Отключить авто-режим"))
async def disable_auto_mode(message: types.Message):
    global auto_mode
    auto_mode = False

    keyboard = await current_keyboard(auto_mode)

    await message.answer("Авто-режим отключен", reply_markup=keyboard)


@dp.message_handler(Text(equals="Последние 10 новостей"))
async def last_ten_news(message: types.Message):
    get_data()

    with open("news.json", encoding="utf-8") as file:
        all_news = json.load(file)

    keyboard = await current_keyboard(auto_mode)

    await message.answer("Последние 10 новостей ФК Зенит", reply_markup=keyboard)

    for k, v in sorted(all_news.items()):
        news = f"{hbold('Дата публикации:', v['Дата публикации'])}\n" \
               f"{hlink(v['Заголовок'], v['Ссылка'])}"

        await message.answer(news, disable_notification=True)


@dp.message_handler(content_types=ContentType.ANY)
async def send_message(message: types.Message):
    await message.reply("К сожалению, у меня нет ответа на это сообщение... "
                        "Чтобы взаимодействовать со мной, используйте кнопки и команды. ")


if __name__ == '__main__':
    executor.start_polling(dp)
