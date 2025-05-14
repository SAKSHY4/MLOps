# app.py - Simple Flask ML API
from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# We'll create a dummy model for now
with open('model.pkl', 'rb') as f:
     model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)[0]
    return jsonify({'prediction': prediction})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/')
def home():
    return "MLOps Flask API running. Use /predict for predictions or /health for status."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)