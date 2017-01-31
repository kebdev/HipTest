from flask import Flask, jsonify, request

from msg import extract_content, get_load

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello Atlassian</h1>'


@app.route('/health')
def health():
    cpu, hdd, network, virtmem = get_load()
    return jsonify(cpu=cpu, hdd=hdd, network=network, virtmem=virtmem)


@app.route('/api/msg', methods=['GET'])
def get_content():
    mentions, emoticons, links = extract_content(request.query_string)
    return jsonify(mentions=mentions, emoticons=emoticons, links=links)


if __name__ == '__main__':
    app.run(debug=False)    # change to True if debugging locally



