#!/usr/bin/python3
"""
File: server.py
Author: Elizabeth Trinh
Purpose:
	Takes requests and returns data relating to the request.
"""

from flask import Flask, request
import os
import requests
from df_response_lib import *

app = Flask(__name__)


@app.route('/')
def serve_homepage():
    return 'homepage'

def serve_zone(param):
    return 'zone'

@app.route('/webhook', methods=['GET', 'POST'])
def serve_webhook():
    # build a request object
    req = request.get_json(force=True)
    # fetch action from json
    action = req.get('queryResult').get('action')
    if action == "findzone.findzone-custom":
        serve_zone(req.get('queryResult').get('parameters'))
    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)