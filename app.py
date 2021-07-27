#!/usr/bin/env python3
from flask import Flask, request, json

import utils as u


app = Flask(__name__)

@app.route('/', methods=['POST'])
def on_event():
    """Handles an event from Google Chat."""
    event_dict = request.get_json()
    filtered_event_dict = u.create_filtered_dict(event_dict)
    values = [
        filtered_event_dict['email'],
        filtered_event_dict['room_id'],
        filtered_event_dict['room_name'],
        filtered_event_dict['thread_id'],
        filtered_event_dict['message'],
        filtered_event_dict['is_first_responder'],
        filtered_event_dict['timestamp'],
        ]
    u.update_google_spreadsheet(values)
    return json.jsonify({'text': str(event_dict)})
    
if __name__ == '__main__':
    print("Hello")
    app.run(port=8000, debug=True)
