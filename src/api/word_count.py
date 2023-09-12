from flask import Flask, jsonify, request

import os
import re

host = os.environ['HOST']
port = os.environ['PORT']

app = Flask(__name__)


def find_words(text: str):
    return re.findall(r'\w+', text)


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Process sentiment analysis and return the length of words in text.
    :return: Jsonified response with length of words in text.
    """
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Invalid request body'}), 400

    if len(text) > 4096:
        return jsonify({'error': 'Invalid text size'}), 400

    words = find_words(text)
    return jsonify({'message': str(len(words))}), 200


if __name__ == '__main__':
    app.run(host=host, port=int(port), debug=True)
