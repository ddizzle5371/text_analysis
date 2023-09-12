from flask import Flask, jsonify, request

import redis
import os

host = os.environ['HOST']
port = os.environ['PORT']

app = Flask(__name__)
registry = redis.Redis(host="registry")


@app.route('/services', methods=['GET'])
def list_services():
    services = {k.decode('utf-8'): registry.get(k).decode('utf-8') for k in registry.keys()}
    return jsonify({'message': services}), 200


@app.route('/services', methods=['POST'])
def register_service():
    data = request.get_json()
    service_name = data.get('service')
    service_url = data.get('url')

    if not service_name or not service_url:
        return jsonify({'error': 'Invalid request body'}), 400

    try:
        registry.set(service_name, service_url)
        return jsonify({'message': f'{service_name} is successfully registered to the registry'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/services/<service_name>', methods=['DELETE'])
def remove_service(service_name):
    try:
        registry.delete(service_name)
        return jsonify({'message': f'{service_name} is successfully removed from the registry'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host=host, port=int(port), debug=True)
