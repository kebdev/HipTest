from flask import Flask, jsonify
from bs4 import BeautifulSoup
import re
import urllib3

from msg import extract_content

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello Atlassian</h1>'

@app.route('/content/<string:chat_msg>')
def get_content(chat_msg):
    mentions, emoticons, links = extract_content(chat_msg)
    return jsonify(mentions=mentions, emoticons=emoticons, links=links)


if __name__ == '__main__':
    app.run(debug=False)    # change to True if debugging locally



