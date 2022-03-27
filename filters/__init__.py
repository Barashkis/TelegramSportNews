from aiogram import Dispatcher
from .news_filter import LastNews


def setup(dp: Dispatcher):
    dp.filters_factory.bind(LastNews)
