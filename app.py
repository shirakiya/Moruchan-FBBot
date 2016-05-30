# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import request

app = Flask(__name__)
ENV = os.getenv('ENV')
if ENV != 'production':
    app.config['DEBUG'] = True

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
    print(req)
    return

if __name__ == '__main__':
    app.run()
