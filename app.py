#!/usr/bin/env python3
"""Example bot that returns a synchronous response."""

from flask import Flask, request, json
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def on_event():
  """Handles an event from Google Chat."""
  event = request.get_json()
  if event['type'] == 'MESSAGE':
    text = str(event)
  else:
    return str(event)
  return json.jsonify({'text': text})
    

if __name__ == '__main__':
    # scopes = [c.READ_WRITE_SCOPE]
    # oauth_credentials = GoogleCredentials(c.TOKEN_JSON_FILE, c.CREDENTIALS_JSON_FILE, scopes).get_oauth_credentials()
    # service = GoogleService(oauth_credentials, c.GOOGLE_PRODUCT, c.PRODUCT_VERSION)
    # values = ['Test', 'Test 2', 'Test 10',]
    # body = h.create_values_dict(values)
    # service.insert_row_into_spreadsheet(body, c.SPREADSHEET_ID, c.SHEET_RANGE, c.VALUE_INPUT_OPTION)
    app.run(port=8080, debug=True)