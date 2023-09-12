from src.api.sentiment_analysis import app
import pytest


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_analyze_success(test_client):
    data = {"text": "example text"}
    response = test_client.post('/analyze', json=data)

    assert response.status_code == 200


def test_analyze_invalid_text_lenth(test_client):
    data = {"text": "long_text" * 5000}
    response = test_client.post('/analyze', json=data)

    assert response.status_code == 400


def test_analyze_missing_text(test_client):
    data = {}
    response = test_client.post('/analyze', json=data)

    assert response.status_code == 400
