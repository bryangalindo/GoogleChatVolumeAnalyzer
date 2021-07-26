#!/usr/bin/env python3
"""Example bot that returns a synchronous response."""

from flask import Flask, request, json

from common import (constants, helpers)
from models import (GoogleCredentials, GoogleService)

app = Flask(__name__)

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
    event = request.get_json()
    text = str(event)
    update_google_spreadsheet(text)
    return json.jsonify({'text': text})
    

if __name__ == '__main__':
    # scopes = [c.READ_WRITE_SCOPE]
    # oauth_credentials = GoogleCredentials(c.TOKEN_JSON_FILE, c.CREDENTIALS_JSON_FILE, scopes).get_oauth_credentials()
    # service = GoogleService(oauth_credentials, c.GOOGLE_PRODUCT, c.PRODUCT_VERSION)
    # values = ['Test', 'Test 2', 'Test 10',]
    # body = h.create_values_dict(values)
    # service.insert_row_into_spreadsheet(body, c.SPREADSHEET_ID, c.SHEET_RANGE, c.VALUE_INPUT_OPTION)
    app.run(port=8080, debug=True)