# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import request
import requests

app = Flask(__name__)
ENV = os.getenv('ENV')
if ENV != 'production':
    app.config['DEBUG'] = True

def send_text_message(sender_id, text):
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

    url = 'https://graph.facebook.com/v2.6/me/messages'
    access_token = {'access_token': ACCESS_TOKEN}
    payload = {
        'recipient': {'id': sender_id},
        'message': {'text': text},
    }

    try:
        res = requests.post(url, params=access_token,
                            json=payload)
        print(res.content)
    except Exception as e:
        print('ERROR: ' + str(e))
        return False
    return True


@app.route('/webhook', methods=['GET'])
def varification():
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if verify_token == VERIFY_TOKEN:
        return challenge
    return 'Error, wrong validation token'

@app.route('/webhook', methods=['POST'])
def callback():
    req = request.get_json(cache=False)
    for entry in req['entry']:
        for event in entry['messaging']:
            sender_id = event['sender']['id']
            if 'message' in event and 'text' in event['message']:
                text = event['message']['text']
                result = send_text_message(sender_id, text)
    return 'OK'

if __name__ == '__main__':
    app.run()
