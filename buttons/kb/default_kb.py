from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Send Contact", request_contact=True)
        ]

    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

kb_cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="cancel")
        ]

        ],
    resize_keyboard=True,
    one_time_keyboard=True
)

kb_weight = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="60KG"),
            KeyboardButton(text="66KG"),
            KeyboardButton(text="73KG"),
            KeyboardButton(text="81KG")
        ],


        [
            KeyboardButton(text="90KG"),
            KeyboardButton(text="100KG"),
            KeyboardButton(text="100Kg"),
        ],
        [
            KeyboardButton(text="cancel")
        ]


    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

#60, 66, 73, 81, 90, 100, +100 кг.