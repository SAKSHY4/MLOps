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
    try:
        data = request.json
        if not data or 'features' not in data:
            return jsonify({"error": "Missing features parameter"}), 400
            
        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features)[0]
        return jsonify({'prediction': float(prediction)})
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/')
def home():
    return "MLOps Flask API running. Use /predict for predictions or /health for status."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)