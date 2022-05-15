from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Update
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text, CommandStart, CommandHelp

import asyncio

from keyboards import current_keyboard
from loader import dp, bot

from filters import LastNews
from main import get_data, get_fresh_data
from states import SportNews


async def get_fresh_news_period():
    while True:
        state = dp.current_state()
        data = await state.get_data()
        auto_mode = data["auto_mode"]
        user_id = data["user_id"]

        if auto_mode:
            await asyncio.sleep(60)

            fresh_news = await get_fresh_data(dp)

            if len(fresh_news) >= 1:
                await get_data(dp)

                for k, v in sorted(fresh_news.items()):
                    news = f"{hlink(v['Заголовок'], v['Ссылка'])}"

                    await bot.send_message(user_id, news)
        else:
            break


@dp.message_handler(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await SportNews.custom.set()

    data = await state.get_data()
    news_count = data.get("news_count")

    if news_count is None:
        news_count = 10
        await state.update_data({
            "news_count": news_count
        })

    await state.reset_state(with_data=False)

    data = await state.get_data()
    all_news = data.get("news_data")
    auto_mode = data.get("auto_mode")
    user_id = data.get("user_id")

    if auto_mode is None:
        await state.update_data({
            "auto_mode": False
        })

    if all_news is None:
        await get_data(dp)

    if user_id is None:
        await state.update_data({
            "user_id": message.from_user.id
        })

    keyboard = await current_keyboard(dp)
    await message.answer("Добро пожаловать, дорогой болельщик Зенита! Здесь ты можешь оперативно следить "
                         "за новостями футбольного клуба Зенит. Пользуйся мной с удовольствием!\n\n"
                         "Чтобы узнать о моем функционале, воспользуйся командой /help",
                         reply_markup=keyboard)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer("Мой функционал:\n"
                         f"1. {hbold('Свежие новости')} покажет все новости, которые я еще не показывал\n"
                         f"2. {hbold('Включить/выключить авто-режим')} позволяет мне автоматически проверять "
                         "вышедшие новости. Также можно отключить эту функцию\n"
                         f"3. {hbold('Настройка')} позволяет изменить количество выводимых мной новостей\n"
                         f"4. {hbold('Последние новости (N шт.)')} покажет последние N новостей\n")


@dp.message_handler(Text(equals="Настройка"))
async def bot_settings(message: types.Message):
    await message.answer("Тут вы можете выбрать нужное вам количество новостей, которое я буду тебе отправлять.\n"
                         "Введи число от 1 до 50 включительно (большее количество я пока не поддерживаю)")

    await SportNews.custom.set()


@dp.message_handler(state=SportNews.custom)
async def set_custom_news_count(message: types.Message, state: FSMContext):
    news_count = int(message.text)
    if not (1 <= news_count <= 50):
        raise ValueError

    await state.update_data({
        "news_count": news_count
    })

    await state.reset_state(with_data=False)

    await get_data(dp)

    keyboard = await current_keyboard(dp)
    await message.answer("Настройка прошла успешно", reply_markup=keyboard)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = await get_fresh_data(dp)

    if len(fresh_news) >= 1:
        await get_data(dp)

        for k, v in sorted(fresh_news.items()):
            news = f"{hlink(v['Заголовок'], v['Ссылка'])}"

            await message.answer(news)
    else:
        await message.answer("Пока нет свежих новостей...")


@dp.message_handler(Text(equals="Включить авто-режим"))
async def enable_auto_mode(message: types.Message, state: FSMContext):
    await state.update_data({
        "auto_mode": True
    })

    loop = asyncio.get_event_loop()
    loop.create_task(get_fresh_news_period())

    keyboard = await current_keyboard(dp)
    await message.answer("Авто-режим включен", reply_markup=keyboard)


@dp.message_handler(Text(equals="Отключить авто-режим"))
async def disable_auto_mode(message: types.Message, state: FSMContext):
    await state.update_data({
        "auto_mode": False
    })

    keyboard = await current_keyboard(dp)
    await message.answer("Авто-режим отключен", reply_markup=keyboard)


@dp.message_handler(LastNews())
async def last_news(message: types.Message, state: FSMContext):
    await get_data(dp)

    data = await state.get_data()
    all_news = data["news_data"]

    for k, v in sorted(all_news.items()):
        news = f"{hlink(v['Заголовок'], v['Ссылка'])}"

        await message.answer(news)


@dp.errors_handler()
async def catch_errors(update: Update, exception):
    if isinstance(exception, ValueError):
        await update.get_current().message.answer("Необходимо ввести число от 1 до 50! Попробуйте ещё раз")


@dp.message_handler(content_types=ContentType.ANY)
async def send_message(message: types.Message):
    await message.answer("К сожалению, у меня нет ответа на это сообщение... "
                         "Чтобы взаимодействовать со мной, используйте кнопки и команды. ")
