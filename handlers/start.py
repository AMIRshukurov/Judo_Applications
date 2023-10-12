import uuid
from aiogram.types import CallbackQuery
from buttons.kb.default_kb import kb_cancel, kb_weight, Phone
from db.Model import save_application, Application, session, check_user_exists
from utils.throtling import rate_limit
from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp, bot
from states.apply import app
from aiogram.dispatcher.filters import Text
import logging
from data.config import chat_id


@dp.message_handler(rate_limit(10), text="/start")
async def start(message: types.Message):
    await message.reply(f"Hello judoka 🥋 !!!:{message.from_user.first_name} \n"
                        f"To apply please fill out the form 📔✍ \n"
                        f"To fill out the form ✍, click on /apply ")


@dp.message_handler(rate_limit(10), text="/apply")
async def name_process(message: types.Message):
    try:
        user_id = message.from_user.id
        if check_user_exists(str(user_id)):
            await message.answer("You are already registered 👀.\n"
                                 "Wait for admin confirmation ☺🙏")
        else:
            await message.reply(f"Enter name ...✍", reply_markup=kb_cancel)
            await app.name.set()

    except Exception as e:
        print(f"Error occurred: {e}")


@dp.message_handler(lambda message: message.text.isdigit(), state=app.name)
async def process_name_invalid(message: types.Message):
    return await message.reply("Wrong type of Name 💩\n Write your correct name 👉(String only !!)👈 ")


@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """

    Allow user to cancel any action

    """

    current_state = await state.get_state()

    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)

    # Cancel state and inform user about it

    await state.finish()

    # And remove keyboard (just in case)

    await message.reply('Cancelled.')


@dp.message_handler(state=app.name)
async def process_name(message: types.Message, state: FSMContext):
    """

    Process user name

    """

    async with state.proxy() as data:
        data['name'] = message.text
    await app.next()

    await message.reply("Great, now enter your last name. \n......✍", reply_markup=kb_cancel)


@dp.message_handler(lambda message: message.text.isdigit(), state=app.surname)
async def process_name_invalid(message: types.Message):
    return await message.reply("Wrong type of Name 💩\n Write your correct name 👉(String only !!)👈 ")


@dp.message_handler(state=app.surname)
async def sername_process(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)

    await app.next()
    await message.reply("Great \n"
                        "Choose your weight category ⚖\n"
                        "Choose your weight from the list below\n"
                        "🔽 🔽 🔽", reply_markup=kb_weight)


@dp.message_handler(lambda message: message.text not in ["60KG", "66KG", "73KG", "81KG", "90KG", "100KG", "100Kg"],
                    state=app.weight)
async def process_room_invalid(message: types.Message):
    return await message.reply("Bad counts of rooms 💩,  👇 choose in keyboard 👇", reply_markup=kb_weight)


@dp.message_handler(state=app.weight)
async def sername_process(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await app.next()
    await message.reply("Now please send your number\n"
                        "Click the button below \n"
                        "🔽 🔽 🔽", reply_markup=Phone)


@dp.message_handler(state=app.contacts, content_types=types.ContentType.CONTACT)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.contact['phone_number']
    await state.update_data(phone=phone)
    await message.reply("To participate,you will need to make a deposit of 100 thousand KRW\n"
                        "To confirm the payment, send a screenshot of the receipt that you paid the amount to the account\n"
                        "Requisites: Тут должен быть номер карты или что ? или расчетный счет ?")
    await app.next()


@dp.message_handler(lambda message: message.text not in ["Send Contact"], state=app.contacts)
async def process_phone_invalid(message: types.Message):
    return await message.reply("Wrong contact !!!\n"
                               "🔽Use button below🔽", reply_markup=Phone)


@dp.message_handler(state=app.photo, content_types=types.ContentType.PHOTO, )
async def procces_get_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    data_1 = await state.get_data()
    name = data_1.get("name")
    surname = data_1.get("surname")
    weight = data_1.get("weight")
    phone = data_1.get("phone")
    photo = data_1.get("photo")
    application = str(uuid.uuid4())
    print(application)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Одобрить", callback_data=f"approve_{application}"))
    keyboard.add(types.InlineKeyboardButton(text="Отклонить", callback_data=f"reject_{application}"))

    await bot.send_photo(chat_id=chat_id, photo=photo,
                         caption=f"Новая заявка на участие в соревнованиях!\n\nИмя: {name}\nФамилия: {surname}\nВес: {weight}\nКонтакт: {phone}",
                         reply_markup=keyboard)
    user = message.from_user.id

    save_application(user_id=user,
                     name=name,
                     surname=surname,
                     weight=weight,
                     contact=phone,
                     photo=photo,
                     application_id=application)

    await message.reply(
        "Your application has been sent to the organizer of the judo competition. \n"
        "The bot will personally send you notifications as soon as the administrator accepts the application.")

    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith("approve_"))
async def process_approve(callback_query: CallbackQuery):
    # Извлекаем идентификатор заявки из callback_data
    application_id = callback_query.data.split('_')[1]

    # Извлекаем идентификатор пользователя из базы данных
    application = session.query(Application).get(application_id)
    user_id = application.user_id

    # Отправляем сообщение пользователю
    await bot.send_message(chat_id=user_id,
                           text=f"Congratulations! Your competition entry has been approved by the Administrator.")

    # Отвечаем на callback_query
    await callback_query.answer(text="Заявка одобрена", show_alert=True)


@dp.callback_query_handler(lambda c: c.data.startswith("reject_"))
async def process_approve(callback_query: CallbackQuery):
    # Извлекаем идентификатор заявки из callback_data
    application_id_to_delete = callback_query.data.split('_')[1]

    # Извлекаем идентификатор пользователя из базы данных
    application = session.query(Application).get(application_id_to_delete )
    user_id = application.user_id
    record_to_delete = session.query(Application).filter_by(application_id=application_id_to_delete).first()

    # Отправляем сообщение пользователю
    await bot.send_message(chat_id=user_id,
                           text=f"Your apprenticeship application has been rejected 😔😕😕\n"
                                f"Make sure you fill out the application correctly and send the correct receipt.\n"
                                f".\n"
                                f".\n"
                                f" Fill out the application again to study\n"
                                f"Press button /apply")

    session.delete(record_to_delete)
    session.commit()

    # Отвечаем на callback_query
    await callback_query.answer(text="Заявка отклонена", show_alert=True)
