import sqlite3
import requests
from config import API_TOKEN, admin

conn = sqlite3.connect('data_base.db')
cur = conn.cursor()



def create_user():
    cur.execute("""create table if not exists users(
        telegram_id int,
        username varchar(50)
    )""")
    
    

def select_user(telegram_id):
    cur.execute("""select * from users where telegram_id = {}""".format(telegram_id))
    user = cur.fetchone()
    return user
    
def add_user(user_id, username):
    user = select_user(user_id)
    if user is None:
        cur.execute("insert into users values('{}', '{}')".format(user_id, username))
        conn.commit()
        text = f"""Bazaga qoshildi
ID : {user_id}
Username: @{username}"""
        response = requests.post(
        url='https://api.telegram.org/bot{}/sendMessage'.format(API_TOKEN),
        data={'chat_id': admin, 'text': text}
        ).json()
    else:
        return False
    
    

def select_all_user():
    cur.execute("select * from users")
    users = cur.fetchall()
    return users


