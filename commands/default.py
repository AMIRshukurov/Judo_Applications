from aiogram import types


async def set_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', "Запустить"),
        types.BotCommand('help', 'Помощь'),
        types.BotCommand('apply', "Запустить")
    ])
