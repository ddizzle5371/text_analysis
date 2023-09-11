from flask import Flask, jsonify, request
from random import randint

app = Flask(__name__)
entities = ["persons", "organizations", "locations"]


@app.route('/entity_recognition', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Invalid request body'}), 400

    return jsonify({'message': entities[randint(0, len(entities) - 1) % len(text)]}), 200


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', debug=True, port=8002)
