from aiogram.dispatcher.filters.state import State, StatesGroup

# User interaction states
class UserData(StatesGroup):
    text = State()  # User entered text to translate

# Admin advertisement flow states
class Admin_rek(StatesGroup):
    rek_check = State()       # Step: choose between photo or video

    rek_photo = State()       # Step: receive photo
    rek_text = State()        # Step: receive text for photo ad
    rek_next = State()        # Step: confirmation before sending photo ad

    rek_video = State()       # Step: receive video
    rek_text1 = State()       # Step: receive text for video ad
    rek_next1 = State()       # Step: confirmation before sending video ad
