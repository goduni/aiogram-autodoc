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


@dp.message_handler(commands=['start'], description='Description for the function with the /start command')
async def start(msg: Message):
    pass


@dp.message_handler(commands=['help'])
async def help(msg: Message):
    """Description for a function with the /help command, using docstring"""
    pass


@dp.message_handler()
async def just_function(msg: Message):
    """Just a function without a command that doesn't output in result"""
    pass


docs = AutoDoc(dp)
docs.parse()
result_as_dict = docs.to_dict()

```