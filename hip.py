from flask import Flask, jsonify, request

from msg import extract_content

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello Atlassian</h1>'


@app.route('/api/msg', methods=['GET'])
def get_content():
    mentions, emoticons, links = extract_content(request.query_string)
    return jsonify(mentions=mentions, emoticons=emoticons, links=links)


if __name__ == '__main__':
    app.run(debug=False)    # change to True if debugging locally



