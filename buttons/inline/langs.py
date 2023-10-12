from aiogram import types


lang_kb = types.InlineKeyboardMarkup()
lang_kb.add(types.InlineKeyboardButton(text="Одобрить", callback_data=f"RU"))
lang_kb.add(types.InlineKeyboardButton(text="Отклонить", callback_data=f"ENG"))

