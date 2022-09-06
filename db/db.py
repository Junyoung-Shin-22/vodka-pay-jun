import gspread
import os

_PATH = os.path.dirname(os.path.realpath(__file__))

_KEY = os.path.join(_PATH, 'vodka-pay-key.json')

with open(os.path.join(_PATH, 'sheet-url.txt')) as f:
    _URL = f.read()

_SERVICE = gspread.service_account(filename=_KEY)
DB = _SERVICE.open_by_url(_URL)

if __name__ == '__main__':
    print(DB)