from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from handlers.tg_bot import dp


class LastNews(BoundFilter):
    async def check(self, message: types.Message):
        state = dp.current_state()
        data = await state.get_data()
        news_count = data["news_count"]

        return message.text == f"Последние новости ({news_count} шт.)"
