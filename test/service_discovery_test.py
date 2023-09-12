from dotenv import load_dotenv

load_dotenv()

from src.api.service_discovery import app
from unittest import mock

import pytest


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_list_services(test_client):
    with mock.patch('src.api.service_discovery.registry.list_all') as mock_list:
        mock_list.return_value = {
            b'entity_recognition': b'http://entity_recognition:8002/analyze',
            b'word_count': b'http://word_count:8004/analyze',
            b'sentiment_analysis': b'http://sentiment_analysis:8003/analyze'
        }
        response = test_client.get('/services')
        assert response.status_code == 200
        assert len(response.get_json()['message']) == 3


@mock.patch('src.api.service_discovery.registry.set')
def test_register_service(mock_set, test_client):
    mock_set.return_value = 1
    response = test_client.post('/services', json={'service': 'entity_recognition', 'url': 'http://entity_recognition:8002/analyze'})
    assert response.status_code == 201


def test_register_service_invalid_request(test_client):
    response = test_client.post('/services', json={})
    assert response.status_code == 400


@mock.patch('src.api.service_discovery.registry.delete')
def test_remove_service(mock_delete, test_client):
    mock_delete.return_value = 1
    response = test_client.delete('/services/entity_recognition')
    assert response.status_code == 200
