from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
registry = redis.Redis(host='localhost', port=6379)


@app.route('/services', methods=['GET'])
def get_services():
    services = [s.decode('utf-8') for s in registry.keys()]
    return jsonify(services), 200


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
    app.run(threaded=True, host='0.0.0.0', debug=True, port=8001)
