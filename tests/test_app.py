import sys
import os
import json
import pytest
import numpy as np

# Add the parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"MLOps Flask API running" in response.data

def test_health(client):
    """
    GIVEN a Flask application
    WHEN the '/health' endpoint is requested (GET)
    THEN check that it returns a healthy status
    """
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_predict(client):
    """
    GIVEN a Flask application
    WHEN a POST request with features is sent to '/predict'
    THEN check that it returns a prediction
    """
    test_data = {"features": [0.5, 0.5, 0.5, 0.5]}
    response = client.post('/predict',
                         json=test_data,
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prediction' in data

def test_predict_bad_request(client):
    """
    GIVEN a Flask application
    WHEN a POST request with missing features is sent to '/predict'
    THEN check that it returns a 400 error
    """
    test_data = {"wrong_key": [0.5, 0.5, 0.5, 0.5]}
    response = client.post('/predict',
                         json=test_data,
                         content_type='application/json')
    assert response.status_code == 400