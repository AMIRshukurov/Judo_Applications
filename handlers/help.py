from aiogram import types
from loader import dp


@dp.message_handler(text="/help")
async def help_procces(message: types.Message):
    await message.answer("This bot is designed to accept applications for participation in Judo competitions.\n"
                         "Where are you required to enter\n"
                         "1) Name\n"
                         "2) Surname\n"
                         "3) Choose your weight category\n"
                         "4) Send your contact number, on which a telegram account is registered\n"
                         "5) Finally, you are required to pay a participation fee.\n"
                         " To confirm that you paid for the participation and were accepted for participation, you will need to send the bot a photo of the receipt confirming that you paid and transferred the money correctly.\n"
                         "After stage 5, the application will be sent to the administrator to confirm the application. \n"
                         "As soon as the application is approved or rejected, the bot will inform you about it.\n"
                         "To start filling out the application, click on /apply")