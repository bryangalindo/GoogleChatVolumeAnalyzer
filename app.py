#!/usr/bin/env python3
import os 

from flask import Flask, request, json
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv

import utils as u

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0
)

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
