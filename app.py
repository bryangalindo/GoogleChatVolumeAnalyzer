#!/usr/bin/env python3
import os 
from logging.config import dictConfig

from flask import Flask, request, json
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv

from common import constants as c
from models.GoogleCredentials import GoogleCredentials
from models.GoogleService import GoogleService
import utils as u

load_dotenv()

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0
)

scopes = [c.READ_WRITE_SCOPE]
creds = GoogleCredentials(c.TOKEN_JSON_FILE, c.CREDENTIALS_JSON_FILE, scopes).get_oauth_credentials()
service = GoogleService(creds, c.GOOGLE_PRODUCT, c.PRODUCT_VERSION)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def on_event():
    """Handles an event from Google Chat."""
    event = request.get_json()
    if event:
        if event.get('type') == c.ADDED:
            room_name = event.get('space', {}).get('displayName')
            app.logger.info(f"Google bot added to {room_name}")
            text = 'Thanks for adding me to *{}*!'.format(room_name if room_name else 'this chat')
        elif event.get('type') == c.MESSAGE:
            app.logger.info(f"Someone mentioned the bot in Google Chat")
            app.logger.info(f"Pulling in list of thread IDs")
            threads = service.read_single_range(c.SPREADSHEET_ID, c.THREAD_ID_SHEET_RANGE)
            app.logger.info(f"Pulled the following list of threads ID: {threads}")
            app.logger.info("Cleaning up event response from Google Chat")
            filtered_event_dict = u.create_filtered_dict(event)
            app.logger.info(f"Response event cleaned. Result: {filtered_event_dict}")
            if filtered_event_dict:
                responder_flag = u.is_first_responder(filtered_event_dict['thread_id'], threads)
                values = [
                    filtered_event_dict.get('email'), filtered_event_dict.get('room_id'),
                    filtered_event_dict.get('room_name'), filtered_event_dict.get('thread_id'),
                    filtered_event_dict.get('message'), responder_flag,
                    filtered_event_dict.get('timestamp'),
                    ]
                app.logger.info(f"Beginning to import {values}")
                u.update_google_spreadsheet(values, service)
                updated_threads = service.read_single_range(c.SPREADSHEET_ID, c.THREAD_ID_SHEET_RANGE)
                if len(updated_threads) > len(threads):
                    app.logger.info(f"Import finished")
                else:
                    app.logger.debug(f"Google Sheets import was not successful.")
                    return json.jsonify({'text': "Error: Your response was not submitted. Please try again"})
                responder_type = 'first responder' if responder_flag == True else 'participator'
                app.logger.info(f"{filtered_event_dict.get('email')} was recorded as a {responder_type}")
                return ''
            else:
                return json.jsonify({'text': "Error: Google did not send your message in the correct format. Please try again."})
        else:
            return "It's been real"
    return ''
    
if __name__ == '__main__':
    app.run(port=8000, debug=True)
