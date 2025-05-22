# app/app.py - Fixed model path for container
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import os

basedir = os.path.dirname(os.path.abspath(__file__))

# Create Flask app with correct template/static paths
app = Flask(__name__, 
           template_folder=os.path.join(basedir, 'templates'),
           static_folder=os.path.join(basedir, 'static'))

model_path = os.path.join(basedir, 'model.pkl')
print(f"Looking for model at: {model_path}")

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except FileNotFoundError as e:
    print(f"Model not found at {model_path}")
    raise e

@app.route('/')
def home():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)