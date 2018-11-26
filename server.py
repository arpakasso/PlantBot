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
from df_response_lib import fulfillment_response

app = Flask(__name__)


@app.route('/')
def serve_homepage():
    return 'homepage'

def serve_zone(param):
    return param

@app.route('/webhook', methods=['POST'])
def serve_webhook():
    fr = fulfillment_response()
    # build a request object
    req = request.get_json(force=True)
    print(req)
    resp = "test"
    # fetch action from json
    action = req.get('queryResult').get('action')
    if action == "findzone.findzone-custom":
        resp = serve_zone(req.get('queryResult').get('parameters'))
    # return a fulfillment response
    return fr.main_response(fulfillment_text=resp)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)