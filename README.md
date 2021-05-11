# aiogram-autodoc

This package allows you to generate documentation for handlers processing commands.

Supports docstrings and filter inside the handler (DescriptionFilter).

Example:
```
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram_autodoc import AutoDoc, DescriptionFilter

bot = Bot('0', validate_token=False)
dp = Dispatcher(bot)

dp.filters_factory.bind(DescriptionFilter)


@dp.message_handler(commands=['start'], description='Описание для функции с командой /start')
async def start(msg: Message):
    pass


@dp.message_handler(commands=['help'])
async def help(msg: Message):
    """Описание для функции с командой /help, с использованием docstring"""
    pass


@dp.message_handler()
async def just_function(msg: Message):
    """Просто функция без команды"""
    pass


docs = AutoDoc(dp)
docs.parse()
result_as_dict = docs.to_dict()
```