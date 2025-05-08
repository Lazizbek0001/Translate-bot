from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Language selection keyboard
lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data='uz'),
            InlineKeyboardButton("🇷🇺 Russian", callback_data='ru'),
            InlineKeyboardButton("🇪🇸 Spanish", callback_data='es')
        ],
        [
            InlineKeyboardButton("🇬🇧 English", callback_data='en'),
            InlineKeyboardButton("🇮🇹 Italian", callback_data='it'),
            InlineKeyboardButton("🇯🇵 Japanese", callback_data='ja')
        ],
        [
            InlineKeyboardButton("🇰🇷 Korean", callback_data='ko'),
            InlineKeyboardButton("🇸🇦 Arabic", callback_data='ar'),
            InlineKeyboardButton("🇨🇳 Chinese", callback_data='zh-cn')
        ],
        [
            InlineKeyboardButton("🇭🇺 Hungarian", callback_data='hu'),
            InlineKeyboardButton("🇫🇷 French", callback_data='fr'),
            InlineKeyboardButton("🇬🇷 Greek", callback_data='el')
        ]
    ]
)

# Confirmation options for sending ad
choose2 = {
    "✅ Ha": 'ha3',
    "❌ Yo‘q": 'yoq3'
}

async def reklama_choose():
    btn = InlineKeyboardMarkup(row_width=2)
    for label, cb_data in choose2.items():
        btn.insert(InlineKeyboardButton(text=label, callback_data=cb_data))
    return btn

# Media type selection for ad
rek = {
    "🖼 Rasm": 'photo',
    "🎥 Video": 'video'
}

async def reklama_p():
    btn = InlineKeyboardMarkup(row_width=2)
    for label, cb_data in rek.items():
        btn.insert(InlineKeyboardButton(text=label, callback_data=cb_data))
    return btn
