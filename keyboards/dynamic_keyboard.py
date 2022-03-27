from aiogram.types import ReplyKeyboardMarkup


async def current_keyboard(dp):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    data = await dp.current_state().get_data()
    news_count = data["news_count"]
    auto_mode = data["auto_mode"]

    buttons_1 = [f"Последние новости ({news_count} шт.)", "Свежие новости"]

    if auto_mode:
        buttons_2 = ["Отключить авто-режим", "Настройка"]
    else:
        buttons_2 = ["Включить авто-режим", "Настройка"]

    keyboard.add(*buttons_1)
    keyboard.add(*buttons_2)

    return keyboard
