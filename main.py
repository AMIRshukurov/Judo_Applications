async def on_startup(dp):

    import filters
    filters.setup(dp)

    import midlware
    midlware.setup(dp)

    from utils.notify_admin import on_start_notify
    await on_start_notify(dp)

    from commands.default import set_commands
    await set_commands(dp)

    print('Бот запущен')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup,skip_updates=True)
