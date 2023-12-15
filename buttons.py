from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("🇺🇿O'zbek🇺🇿", callback_data='uz'),
            InlineKeyboardButton("🇷🇺Russian🇷🇺", callback_data='ru'),
            InlineKeyboardButton("🇪🇸Ispancha🇪🇸", callback_data='es')
        ],
        [
            InlineKeyboardButton("🇬🇧English🇬🇧", callback_data='en'),
            InlineKeyboardButton("🇮🇹Italy🇮🇹", callback_data='it'),
            InlineKeyboardButton("🇯🇵Japan🇯🇵", callback_data='ja')
        ],
        [
            InlineKeyboardButton("🇰🇷Korean🇰🇷", callback_data='ko'),
            InlineKeyboardButton("🇸🇦Arab🇸🇦", callback_data='ar'),
            InlineKeyboardButton("🇨🇳China🇨🇳", callback_data='zh-cn')
        ],
        [
            InlineKeyboardButton("🇭🇺Vengriya🇭🇺", callback_data='hu'),
            InlineKeyboardButton("🇫🇷France🇫🇷", callback_data='fr'),
            InlineKeyboardButton("🇬🇷Greek🇬🇷", callback_data='el')
        ]
    ]
)


choose2 = {"Ha": 'ha3',"Yoq": 'yoq3'}


async def reklama_choose():
    btn = InlineKeyboardMarkup(row_width=2)
    for i,m  in choose2.items():
        btn.insert(InlineKeyboardButton(text=i, callback_data=m))
    return btn


rek = {'Rasm':'photo', 'Video':'video'}


async def reklama_p():
    btn = InlineKeyboardMarkup(row_width=2)
    for i,m  in rek.items():
        btn.insert(InlineKeyboardButton(text=i, callback_data=m))
    return btn