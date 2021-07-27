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
    event = request.get_json()
    if event['type'] == 'ADDED_TO_SPACE' and not event['space']['singleUserBotDm']:
        text = 'Thanks for adding me to "%s"!' % (event['space']['displayName'] if event['space']['displayName'] else 'this chat')
    elif event['type'] == 'MESSAGE':
        filtered_event_dict = u.create_filtered_dict(event)
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
        text = 'Your message has been recorded as "%s"' % ('first responder' if filtered_event_dict['is_first_responder'] else 'participator')
    else:
        return 
    return json.jsonify({'text': text})
    
if __name__ == '__main__':
    print("Hello")
    app.run(port=8000, debug=True)
