#!/usr/bin/python
# -*- coding: utf-8 -*-


async def on_startup(dp):
    """
    Функция выполняется при запуске бота
    """
    print("Бот запущен!")


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
