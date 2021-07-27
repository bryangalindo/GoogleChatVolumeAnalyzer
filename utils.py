from common import (constants, helpers)
from models.GoogleCredentials import GoogleCredentials
from models.GoogleService import GoogleService


scopes = [constants.READ_WRITE_SCOPE]
creds = GoogleCredentials(constants.TOKEN_JSON_FILE, constants.CREDENTIALS_JSON_FILE, scopes)
creds = creds.get_oauth_credentials()
service = GoogleService(creds, constants.GOOGLE_PRODUCT, constants.PRODUCT_VERSION)
threads = service.read_single_range(constants.SPREADSHEET_ID, constants.THREAD_ID_SHEET_RANGE)

def is_first_responder(thread_id: str, threads: list) -> bool:
    if threads and thread_id:
        thread_id_list = helpers.flatten_list(threads)
        if thread_id_list:
            return helpers.string_is_unique(thread_id, threads)

def create_filtered_dict(_dict):
    room_path_list = _dict['message']['thread']['name'].split('/')
    thread_id = room_path_list[3]
    room_id = room_path_list[1]
    responder_flag = is_first_responder(thread_id, threads)
    return {
        'timestamp': _dict['eventTime'],
        'email': _dict['message']['sender']['email'],
        'room_id': room_id,
        'thread_id': thread_id,
        'room_name': _dict['message']['space']['displayName'],
        'message': _dict['message']['argumentText'],
        'is_first_responder': responder_flag
    }

def update_google_spreadsheet(record):
    body = helpers.create_values_dict([record])
    service.insert_row_into_spreadsheet(
        body, 
        constants.SPREADSHEET_ID, 
        constants.SHEET_RANGE, 
        constants.VALUE_INPUT_OPTION
        )