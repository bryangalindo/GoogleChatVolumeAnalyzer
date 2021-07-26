#!/usr/bin/env python3
"""Example bot that returns a synchronous response."""

from flask import Flask, request, json

from common import (constants, helpers)
from models.GoogleCredentials import GoogleCredentials
from models.GoogleService import GoogleService

app = Flask(__name__)

def create_filtered_dict(_dict):
    room_path_list = _dict['message']['thread']['name'].split('/')
    return {
        'timestamp': _dict['eventTime'],
        'email': _dict['message']['sender']['email'],
        'room_id': room_path_list[1],
        'room_thread': room_path_list[3],
        'room_name': _dict['message']['space']['displayName'],
        'message': _dict['message']['argumentText'],
    }

def update_google_spreadsheet(record):
    scopes = [constants.READ_WRITE_SCOPE]
    creds = GoogleCredentials(constants.TOKEN_JSON_FILE, constants.CREDENTIALS_JSON_FILE, scopes)
    creds = creds.get_oauth_credentials()
    service = GoogleService(creds, constants.GOOGLE_PRODUCT, constants.PRODUCT_VERSION)
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
        filtered_event_dict['room_thread'],
        filtered_event_dict['message'],
        filtered_event_dict['timestamp']
        ]
    update_google_spreadsheet(values)
    return json.jsonify({'text': event_dict})
    

if __name__ == '__main__':
    app.run(port=8080, debug=True)
