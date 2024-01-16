import logging
from aiogram import Bot, Dispatcher, executor, types
from googletrans import Translator
from config import *
from buttons import *
import data_base as db
from state import Admin_rek, UserData
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

tr = Translator()
Storage = MemoryStorage()
bot =Bot(token=API_TOKEN)
dp=Dispatcher(bot, storage=Storage)


db.create_user()

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.username)
    
    await message.answer("🇺🇿Tarjima qiladigan so'zni yuboring!\n🇷🇺Отправьте слово для перевода!")
    



@dp.message_handler(commands='users', user_id = admin)
async def exo(message: types.Message):
        users = db.select_all_user()
        text = f"{len(users)} people registered"
        await bot.send_message(admin,text)
        


@dp.message_handler(commands='reklama', user_id = admin)
async def exo(message: types.Message):
    await message.answer("Reklama fileni tanlang ", reply_markup=await reklama_p())
    await Admin_rek.rek_check.set()
    
    
@dp.callback_query_handler(state=Admin_rek.rek_check)
async def send(call: types.CallbackQuery):
    if call.data == 'photo':
        await call.message.answer("Rasmni jo'nating")
        await Admin_rek.rek_photo.set()
    
    
    else:
        await call.message.answer("Video jo'nating")
        await Admin_rek.rek_video.set()
    await call.message.delete()

@dp.message_handler(content_types='video', state=Admin_rek.rek_video)
async def send(message: types.Message, state: FSMContext):
    photo = message.video.file_id
    await state.update_data(rek_video = photo)
    await message.answer("Reklama matn jo'nating")
    await Admin_rek.rek_text1.set()
    
       
    
@dp.message_handler(content_types='photo', state=Admin_rek.rek_photo)
async def send(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(rek_photo = photo)
    await message.answer("Reklama matn jo'nating")
    await Admin_rek.rek_text.set()
    
    
    
    
@dp.message_handler(state=Admin_rek.rek_text1)
async def send(message: types.Message, state: FSMContext):
    
    await state.update_data(rek_text1 = message.text)
    await message.answer("Tekshiring")
    data = await state.get_data()
    vido_ = data.get('rek_video')
    await message.answer_video(video=vido_, caption=message.text, reply_markup= await reklama_choose())
    
    await Admin_rek.rek_next1.set()

@dp.message_handler(state=Admin_rek.rek_text)
async def send(message: types.Message, state: FSMContext):
    
    await state.update_data(rek_text = message.text)
    await message.answer("Tekshiring")
    data = await state.get_data()
    vido_ = data.get('rek_photo')
    await message.answer_photo(photo=vido_, caption=message.text, reply_markup= await reklama_choose())
    
    await Admin_rek.rek_next.set()
    
@dp.callback_query_handler(state=Admin_rek.rek_next)
async def sedn(call: types.CallbackQuery, state: FSMContext):
    
    users = db.select_all_user()
    if call.data == 'ha3':
        data = await state.get_data()
      
        spam_info = 0
        not_spm = 0
        for user in users:
            
            try:
                await bot.send_photo(chat_id=user[0], photo = data.get('rek_photo'), caption= data.get('rek_text')) 
                not_spm +=1
                
            except:
                spam_info +=1

        await bot.send_message(chat_id=admin, text = f"Xabar yetib bormaganlar: {spam_info}\nXabar yetib borganlar: {not_spm}")



    else:
        await call.message.answer("Reklama bekor qilindi")

    await state.finish()
    await state.reset_data()
    await call.message.delete()
        
        
@dp.callback_query_handler(state=Admin_rek.rek_next1)
async def sedn(call: types.CallbackQuery, state: FSMContext):
    
    users = db.select_all_user()
    if call.data == 'ha3':
        data = await state.get_data()
       
        spam_info = 0
        not_spm = 0
        for user in users:
            try:
                await bot.send_video(chat_id=user[0], video = data.get('rek_video'), caption= data.get('rek_text1')) 
                not_spm +=1
            
            except:
                spam_info +=1

        await bot.send_message(chat_id=admin, text = f"Xabar yetib bormaganlar: {spam_info}\nXabar yetib borganlar: {not_spm}")

    else:
        await call.message.answer("Reklama bekor qilindi")

    await state.finish()
    await state.reset_data()
    await call.message.delete()




@dp.message_handler()
async def exo(message: types.Message):
    global text
    text = message.text
    
    await message.answer("Tilni tanlang!!!", reply_markup=lang)
    await UserData.text.set()
 
@dp.callback_query_handler(state=UserData.text)
async def translate(c: types.CallbackQuery, state: FSMContext):
    result = tr.translate(text, dest =c.data)
    await c.message.answer(result.text)
    await state.finish()
    await state.reset_data()
   



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
