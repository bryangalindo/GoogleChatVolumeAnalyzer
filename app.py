#!/usr/bin/env python3
"""Example bot that returns a synchronous response."""

from flask import Flask, request, json
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def on_event():
  """Handles an event from Google Chat."""
  event = request.get_json()
  if event['type'] == 'ADDED_TO_SPACE' and not event['space']['singleUserBotDm']:
    text = 'Thanks for adding me to "%s"!' % (event['space']['displayName'] if event['space']['displayName'] else 'this chat')
  elif event['type'] == 'MESSAGE':
    r = requests.get("https://chat.googleapis.com/v1/spaces/AAAACPVl0EY/messages/")
    text = str(r.content)[:200]
  else:
    return
  return json.jsonify({'text': text})


if __name__ == '__main__':
  app.run(port=8080, debug=True)