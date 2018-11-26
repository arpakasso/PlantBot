#!/usr/bin/python3
"""
File: server.py
Author: Elizabeth Trinh
Purpose:
	Takes requests and returns data relating to the request.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def serve_homepage():
    return 'homepage'


@app.route('/webhook')
def serve_webhook(article):
    return 'webhook'

if __name__ == '__main__':
    app.run(threaded=True)