from common import (constants, helpers)


def is_first_responder(service, thread_id):
    threads = service.read_single_range(constants.SPREADSHEET_ID, constants.THREAD_ID_SHEET_RANGE)
    thread_id_list = helpers.flatten_list(threads)
    if thread_id in thread_id_list:
        return False
    else:
        return True

def create_filtered_dict(service, _dict):
    room_path_list = _dict['message']['thread']['name'].split('/')
    thread_id = room_path_list[3]
    room_id = room_path_list[1]
    responder_flag = is_first_responder(service, thread_id)
    return {
        'timestamp': _dict['eventTime'],
        'email': _dict['message']['sender']['email'],
        'room_id': room_id,
        'thread_id': thread_id,
        'room_name': _dict['message']['space']['displayName'],
        'message': _dict['message']['argumentText'],
        'is_first_responder': responder_flag
    }

def update_google_spreadsheet(service, record):
    body = helpers.create_values_dict([record])
    service.insert_row_into_spreadsheet(
        body, 
        constants.SPREADSHEET_ID, 
        constants.SHEET_RANGE, 
        constants.VALUE_INPUT_OPTION
        )