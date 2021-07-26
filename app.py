#!/usr/bin/env python3
"""Example bot that returns a synchronous response."""

from flask import Flask, request, json

from common import (constants, helpers)
from models.GoogleCredentials import GoogleCredentials
from models.GoogleService import GoogleService

app = Flask(__name__)


scopes = [constants.READ_WRITE_SCOPE]
creds = GoogleCredentials(constants.TOKEN_JSON_FILE, constants.CREDENTIALS_JSON_FILE, scopes)
creds = creds.get_oauth_credentials()
service = GoogleService(creds, constants.GOOGLE_PRODUCT, constants.PRODUCT_VERSION)

def is_first_responder(thread_id):
    threads = service.read_single_range(constants.SPREADSHEET_ID, constants.THREAD_ID_SHEET_RANGE)
    thread_id_list = helpers.flatten_list(threads)
    if thread_id in thread_id_list:
        return True
    else:
        return False

def create_filtered_dict(_dict):
    room_path_list = _dict['message']['thread']['name'].split('/')
    thread_id = room_path_list[3]
    room_id = room_path_list[1]
    is_first_responder = app.is_first_responder(thread_id)
    return {
        'timestamp': _dict['eventTime'],
        'email': _dict['message']['sender']['email'],
        'room_id': room_id,
        'thread_id': thread_id,
        'room_name': _dict['message']['space']['displayName'],
        'message': _dict['message']['argumentText'],
        'is_first_responder': is_first_responder
    }

def update_google_spreadsheet(record):
    body = helpers.create_values_dict([record])
    service.insert_row_into_spreadsheet(
        body, 
        constants.SPREADSHEET_ID, 
        constants.SHEET_RANGE, 
        constants.VALUE_INPUT_OPTION
        )

@app.route('/', methods=['POST'])
def on_event():
    """Handles an event from Google Chat."""
    event_dict = request.get_json()
    filtered_event_dict = create_filtered_dict(event_dict)
    values = [
        filtered_event_dict['email'],
        filtered_event_dict['room_id'],
        filtered_event_dict['room_name'],
        filtered_event_dict['thread_id'],
        filtered_event_dict['message'],
        filtered_event_dict['is_first_responder'],
        filtered_event_dict['timestamp'],
        ]
    update_google_spreadsheet(values)
    return json.jsonify({'text': str(event_dict)})
    

if __name__ == '__main__':
    app.run(port=8080, debug=True)
