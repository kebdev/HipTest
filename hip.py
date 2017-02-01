from flask import Flask, jsonify, request, make_response

from msg import extract_content, get_load
from gzip_deco import gzipped

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return '<h1>Hello Atlassian</h1>'


@app.route('/health', methods=['GET'])
@gzipped
def health():
    load_stats = get_load()
    return load_stats, 200, {'Content-Type': 'application/json'}


@app.route('/api/msg', methods=['GET'])
@gzipped
def get_content():
    content = extract_content(request.query_string)
    return content, 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)    # change to True if debugging locally



