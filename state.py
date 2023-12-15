from aiogram.dispatcher.filters.state import State, StatesGroup


class UserData(StatesGroup):
    text = State()

class Admin_rek(StatesGroup):
    
    rek_photo = State()
    rek_text = State()
    rek_video = State()
    rek_check = State()
    
    rek_text1 = State()
    
    rek_next = State()
    rek_next1 = State()