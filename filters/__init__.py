from aiogram import Dispatcher

from .rate_limit import IsPrivate


def setup(dp:Dispatcher):
    dp.filters_factory.bind(IsPrivate)