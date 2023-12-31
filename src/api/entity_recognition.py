from flask import Flask, jsonify, request

import os

host = os.environ['HOST']
port = os.environ['PORT']
entities = ["persons", "organizations", "locations"]

app = Flask(__name__)


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Process entity recognition analysis on text and return the result. For now, it has a predefined
    way to generate the result with the modulo operation.
    :return: Jsonified response with entity recognition result
    """
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Invalid request body'}), 400

    if len(text) > 4096:
        return jsonify({'error': 'Invalid text size'}), 400

    return jsonify({'message': entities[(len(entities) - 1) % len(text)]}), 200


if __name__ == '__main__':
    app.run(host=host, port=int(port), debug=True)
