from flask import Flask, jsonify, request

import os

host = os.environ['HOST']
port = os.environ['PORT']
sentiments = ["positive", "neutral", "negative"]

app = Flask(__name__)


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Process sentiment analysis and return the result. For now, it has a predefined
    way to generate the result with the modulo operation.
    :return: Jsonified response with a sentiment analysis result
    """
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Invalid request body'}), 400

    if len(text) > 4096:
        return jsonify({'error': 'Invalid text size'}), 400

    return jsonify({'message': sentiments[(len(sentiments) - 1) % len(text)]}), 200


if __name__ == '__main__':
    app.run(host=host, port=int(port), debug=True)
