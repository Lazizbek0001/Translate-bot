import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from googletrans import Translator

from config import API_TOKEN, admin
from buttons import lang, reklama_p, reklama_choose
import data_base as db
from state import Admin_rek, UserData

# Init
tr = Translator()
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Logging
logging.basicConfig(level=logging.INFO)

# Create DB
db.create_user()

# /start handler
@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.username)
    await message.answer("🇺🇿Tarjima qiladigan so'zni yuboring!\n🇷🇺Отправьте слово для перевода!")
    print(f"{message.chat.id}")
    await bot.send_message(chat_id=-1002125090677, text="Vhrass")


# /users (admin only)
@dp.message_handler(commands='users', user_id=admin)
async def show_users(message: types.Message):
    users = db.select_all_user()
    await message.answer(f"{len(users)} people registered")

# /reklama (admin only)
@dp.message_handler(commands='reklama', user_id=admin)
async def reklama_start(message: types.Message):
    await message.answer("Reklama turini tanlang", reply_markup=await reklama_p())
    await Admin_rek.rek_check.set()

# Reklama type handler
@dp.callback_query_handler(state=Admin_rek.rek_check)
async def reklama_type(call: types.CallbackQuery):
    if call.data == 'photo':
        await call.message.answer("Rasmni jo'nating")
        await Admin_rek.rek_photo.set()
    else:
        await call.message.answer("Videoni jo'nating")
        await Admin_rek.rek_video.set()
    await call.message.delete()

# Handle photo
@dp.message_handler(content_types='photo', state=Admin_rek.rek_photo)
async def get_rek_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(rek_photo=photo)
    await message.answer("Reklama matnini kiriting")
    await Admin_rek.rek_text.set()

# Handle video
@dp.message_handler(content_types='video', state=Admin_rek.rek_video)
async def get_rek_video(message: types.Message, state: FSMContext):
    video = message.video.file_id
    await state.update_data(rek_video=video)
    await message.answer("Reklama matnini kiriting")
    await Admin_rek.rek_text1.set()

# Confirm text for photo ad
@dp.message_handler(state=Admin_rek.rek_text)
async def confirm_photo_text(message: types.Message, state: FSMContext):
    await state.update_data(rek_text=message.text)
    data = await state.get_data()
    await message.answer_photo(photo=data['rek_photo'], caption=message.text, reply_markup=await reklama_choose())
    await Admin_rek.rek_next.set()

# Confirm text for video ad
@dp.message_handler(state=Admin_rek.rek_text1)
async def confirm_video_text(message: types.Message, state: FSMContext):
    await state.update_data(rek_text1=message.text)
    data = await state.get_data()
    await message.answer_video(video=data['rek_video'], caption=message.text, reply_markup=await reklama_choose())
    await Admin_rek.rek_next1.set()

# Send photo ad to users
@dp.callback_query_handler(state=Admin_rek.rek_next)
async def send_photo_ad(call: types.CallbackQuery, state: FSMContext):
    users = db.select_all_user()
    data = await state.get_data()
    sent, failed = 0, 0

    if call.data == 'ha3':
        for user in users:
            try:
                await bot.send_photo(chat_id=user[0], photo=data['rek_photo'], caption=data['rek_text'])
                sent += 1
            except:
                failed += 1
        await bot.send_message(admin, f"✅ Sent: {sent}\n❌ Failed: {failed}")
    else:
        await call.message.answer("Reklama bekor qilindi")

    await state.finish()
    await call.message.delete()

# Send video ad to users
@dp.callback_query_handler(state=Admin_rek.rek_next1)
async def send_video_ad(call: types.CallbackQuery, state: FSMContext):
    users = db.select_all_user()
    data = await state.get_data()
    sent, failed = 0, 0

    if call.data == 'ha3':
        for user in users:
            try:
                await bot.send_video(chat_id=user[0], video=data['rek_video'], caption=data['rek_text1'])
                sent += 1
            except:
                failed += 1
        await bot.send_message(admin, f"✅ Sent: {sent}\n❌ Failed: {failed}")
    else:
        await call.message.answer("Reklama bekor qilindi")

    await state.finish()
    await call.message.delete()

# Message translator start
@dp.message_handler()
async def ask_language(message: types.Message):
    global text
    text = message.text
    await message.answer("Tilni tanlang!", reply_markup=lang)
    await UserData.text.set()

# Language selection and translation
@dp.callback_query_handler(state=UserData.text)
async def handle_language_selection(call: types.CallbackQuery, state: FSMContext):
    result = await tr.translate(text, dest=call.data)  # ✅ Await the coroutine
    await call.message.delete()
    await call.message.answer(result.text)
    await state.finish()

# Start polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
