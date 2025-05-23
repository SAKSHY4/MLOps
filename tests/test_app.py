import sys
import os
import json
import pytest
import numpy as np

sys.path.insert(0, '/app')

# Now this import will work in the container
from app import app

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
    # Check for HTML content since you're serving templates
    assert b"<html" in response.data or b"<!DOCTYPE" in response.data

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
    # Use 0-10 range values that work with your model
    test_data = {"features": [5.0, 3.0, 7.0, 8.0]}
    response = client.post('/predict',
                         json=test_data,
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prediction' in data
    # Check prediction is valid (0 or 1)
    assert data['prediction'] in [0, 1]

def test_predict_bad_request(client):
    """
    GIVEN a Flask application
    WHEN a POST request with missing features is sent to '/predict'
    THEN check that it returns a 400 error
    """
    test_data = {"wrong_key": [5.0, 3.0, 7.0, 8.0]}
    response = client.post('/predict',
                         json=test_data,
                         content_type='application/json')
    assert response.status_code == 400