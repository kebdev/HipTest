from flask import Flask, jsonify
from bs4 import BeautifulSoup
import re
import urllib3

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello Atlassian</h1>'

@app.route('/content/<string:chat_msg>')
def get_content(chat_msg):
    mentions = get_mentions(chat_msg)
    emoticons = get_emoticons(chat_msg)
    links = get_links(chat_msg)
    return jsonify(mentions=mentions, emoticons=emoticons, links=links)

def get_mentions(chat_msg):
    mentions = re.findall('@[a-zA-Z]{1,15}', chat_msg)
    return mentions   # TODO: remove @ sign from names

def get_emoticons(chat_msg):
    emoticons = re.findall('\([a-zA-Z]{1,15}\)', chat_msg)
    return emoticons  # TODO: remove parentheses from emoticons

def get_links(chat_msg):
    # regex = '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)'
    # links = re.findall(regex, chat_msg)
    # TODO: could not get this to work! Find a better regex, or use a POST instead of a GET and put it in the body of the POST

    http = urllib3.PoolManager()
    
    link_titles = []
    links = ['https://twitter.com/jdorfman/status/430511497475670016', 'https://www.google.com']
    for link in links:
        r = http.request('GET', link)
        if r.status == 200 or r.status == 201:
            soup = BeautifulSoup(r.data)
            link_title = { 
                'url': link, 
                'title': soup.title.string
            }
            link_titles.append(link_title)
 
    return link_titles

if __name__ == '__main__':
    app.run(debug=False)    # change to True if debugging locally



