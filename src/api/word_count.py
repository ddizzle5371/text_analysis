from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/word_count', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Invalid request body'}), 400

    words = text.split()
    return jsonify({'message': str(len(words))}), 200


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', debug=True, port=8004)
