from dotenv import load_dotenv

load_dotenv()

from src.api.main import app
from unittest import mock

import pytest
import requests.exceptions


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@mock.patch('src.api.main.redis.Redis.get')
@mock.patch('src.api.main.requests.post')
def test_analyze_success(mock_post, mock_get, test_client):
    mock_get.return_value = 'http://entity_recognition:8002/analyze'
    mock_post.return_value.json.return_value = {'result': 'success'}

    response = test_client.post('/analyze', json={'service': 'entity_recognition', 'text': 'Stone Island'})

    assert response.status_code == 200


@mock.patch('src.api.main.redis.Redis.get')
@mock.patch('src.api.main.requests.post')
def test_analyze_server_error(mock_post, mock_get, test_client):
    mock_get.return_value = 'http://entity_recognition:8002/analyze'
    mock_post.side_effect = requests.exceptions.ConnectionError

    response = test_client.post('/analyze', json={'service': 'entity_recognition', 'text': 'Stone Island'})

    assert response.status_code == 500


def test_analyze_invalid_request(test_client):
    response = test_client.post('/analyze', json={'service': 'entity_recognition'})
    assert response.status_code == 400


@mock.patch('src.api.main.redis.Redis.get')
def test_analyze_invalid_service_url(mock_get, test_client):
    mock_get.return_value = None
    response = test_client.post('/analyze', json={'service': 'entity_recognition', 'text': 'Stone Island'})
    assert response.status_code == 404
