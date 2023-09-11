from flask import Flask, jsonify, request

import os

host = os.environ['HOST']
port = os.environ['PORT']
sentiments = ["positive", "neutral", "negative"]

app = Flask(__name__)


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Invalid request body'}), 400

    return jsonify({'message': sentiments[(len(sentiments) - 1) % len(text)]}), 200


if __name__ == '__main__':
    app.run(host=host, port=int(port), debug=True)
