import os

from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_RANGE = 'Sheet2'
READ_WRITE_SCOPE = 'https://www.googleapis.com/auth/spreadsheets'
TOKEN_JSON_FILE = 'token.json'
CREDENTIALS_JSON_FILE = 'credentials.json'
GOOGLE_PRODUCT = 'sheets'
PRODUCT_VERSION = 'v4'
VALUE_INPUT_OPTION = 'RAW'
THREAD_ID_SHEET_RANGE = 'Sheet2!D:D'
ROOM_ID_INDEX = 1
THREAD_ID_INDEX = 3