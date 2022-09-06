import gspread
import os

_PATH = os.path.dirname(os.path.realpath(__file__))

_KEY = os.path.join(_PATH, 'vodka-pay-key.json')

with open(os.path.join(_PATH, 'sheet-url.txt')) as f:
    _URL = f.read()

_SERVICE = gspread.service_account(filename=_KEY)
DB = _SERVICE.open_by_url(_URL)

DB_USERS = DB.worksheet('users')

def db_get_users_data():
    return DB_USERS.get_all_values()

def db_get_users_id():
    return [user[0] for user in db_get_users_data()]

def db_add_user(id, account):
    data = db_get_users_data()
    data.append([id, account])

    DB_USERS.update('A1', data)

if __name__ == '__main__':
    db_add_user(2, 26)