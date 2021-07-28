from common import constants as c
from common import helpers as h


def is_first_responder(thread_id: str, threads: list) -> bool:
    if threads and thread_id:
        thread_id_list = h.flatten_list(threads)
        if thread_id_list:
            return h.string_is_unique(thread_id, thread_id_list)

def create_filtered_dict(_dict: dict) -> dict:
    root_message_dict = _dict.get('message')
    if root_message_dict:
        room_parameters = root_message_dict['thread']['name'].split('/')
        thread_id = room_parameters[3]
        room_id = room_parameters[1]
        return {
            'timestamp': _dict['eventTime'],
            'email': root_message_dict['sender']['email'],
            'room_id': room_id,
            'thread_id': thread_id,
            'room_name': root_message_dict['space']['displayName'],
            'message': root_message_dict['argumentText'],
            'user_id': root_message_dict['sender']['name'],
        }

def update_google_spreadsheet(record, service):
    body = h.create_values_dict([record])
    service.insert_row_into_spreadsheet(
        body, 
        c.SPREADSHEET_ID, 
        c.SHEET_RANGE, 
        c.VALUE_INPUT_OPTION
        )