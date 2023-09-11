from flask import Flask, jsonify, request
import requests
import redis

app = Flask(__name__)
registry = redis.Redis(host='localhost', port=6379)


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    service_name = data.get('service')
    text = data.get('text')

    if not service_name or not text:
        return jsonify({'error': 'Invalid request body'}), 400

    if len(text) > 4096:
        return jsonify({'error': 'Invalid text size'}), 400

    service_url = registry.get(service_name).decode('utf-8')

    if not service_url:
        return jsonify({'message': f'{service_name} not found'}), 404

    try:
        response = requests.post(service_url, json=data)
        return response.json()
    except KeyError:
        return jsonify({'error': 'Service does not exist in the registry'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', debug=True, port=8000)
