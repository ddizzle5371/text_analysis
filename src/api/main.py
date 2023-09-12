from flask import Flask, jsonify, request
from src.lib.service_registry import ServiceRegistry

import requests
import os

host = os.environ['HOST']
port = os.environ['PORT']
service_registry_host = os.environ['SERVICE_REGISTRY_HOST']
service_registry_port = os.environ['SERVICE_REGISTRY_PORT']

app = Flask(__name__)
registry = ServiceRegistry(host=service_registry_host, port=service_registry_port)


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    service_name = data.get('service')
    text = data.get('text')

    if not service_name or not text:
        return jsonify({'error': 'Invalid request body'}), 400

    service_url = registry.get(service_name)

    if not service_url:
        return jsonify({'error': f'{service_name} does not exist in the registry'}), 404

    try:
        response = requests.post(service_url, json=data)
        return response.json()
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host=host, port=int(port), debug=True)
