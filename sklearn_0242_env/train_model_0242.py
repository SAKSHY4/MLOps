# train_model_user_friendly.py - 0-10 Range MLOps Model
import pickle
import numpy as np
import json
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix

def train_user_friendly_model():
    """
    Train ML model with user-friendly 0-10 input ranges and binary output
    Perfect for web frontend testing and user interaction
    """
    print("=== User-Friendly MLOps Model Training (0-10 Range) ===")
    
    # 1. Generate synthetic dataset
    print("1. Generating synthetic dataset...")
    X, y = make_classification(
        n_samples=2000,           # More samples for better training
        n_features=4,             # 4 features to match your API
        n_informative=3,          # 3 informative features
        n_redundant=1,            # 1 redundant feature
        n_clusters_per_class=1,   # Single cluster per class
        class_sep=1.5,            # Good class separation
        random_state=42           # Reproducible results
    )
    
    print(f"   Raw dataset shape: {X.shape}")
    print(f"   Classes: {np.unique(y)}")
    print(f"   Class distribution: {np.bincount(y)}")
    
    # 2. Scale features to user-friendly 0-10 range
    print("2. Scaling features to 0-10 range...")
    scaler = MinMaxScaler(feature_range=(0, 10))
    X_scaled = scaler.fit_transform(X)
    
    print(f"   Feature ranges after scaling:")
    for i in range(X_scaled.shape[1]):
        print(f"     Feature {i+1}: [{X_scaled[:, i].min():.1f}, {X_scaled[:, i].max():.1f}]")
    
    # 3. Split into train and test sets
    print("3. Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Train RandomForest model
    print("4. Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,         # Many trees for stability
        max_depth=10,             # Prevent overfitting
        min_samples_split=5,      # Conservative splits
        min_samples_leaf=2,       # Leaf size control
        random_state=42           # Reproducible results
    )
    
    model.fit(X_train, y_train)
    
    # 5. Evaluate model performance
    print("5. Evaluating model...")
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    
    print(f"   Training accuracy: {train_accuracy:.4f}")
    print(f"   Test accuracy: {test_accuracy:.4f}")
    
    # 6. Test with user-friendly values
    print("6. Testing with user-friendly input ranges...")
    test_cases = [
        [5.0, 5.0, 5.0, 5.0],     # Middle values
        [2.0, 3.0, 7.0, 8.0],     # Mixed values
        [1.0, 1.0, 9.0, 9.0],     # Extreme combinations
        [7.5, 2.5, 4.0, 6.0],     # Random valid values
        [9.0, 8.0, 1.0, 2.0],     # Different pattern
    ]
    
    predictions_summary = []
    for i, test_input in enumerate(test_cases):
        prediction = model.predict([test_input])[0]
        probability = model.predict_proba([test_input])[0]
        confidence = probability.max()
        
        print(f"   Test {i+1}: {test_input} → Class {prediction} (confidence: {confidence:.3f})")
        predictions_summary.append({
            'input': test_input,
            'prediction': int(prediction),
            'confidence': float(confidence)
        })
    
    # 7. Feature importance analysis
    print("7. Feature importance:")
    feature_importance = {}
    for i, importance in enumerate(model.feature_importances_):
        print(f"   Feature {i+1}: {importance:.3f}")
        feature_importance[f'feature_{i+1}'] = float(importance)
    
    # 8. Generate detailed evaluation
    y_pred = model.predict(X_test)
    print("\n8. Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # 9. Save model and comprehensive metadata
    print("9. Saving model and metadata...")
    
    # Save the trained model
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Save scaler for potential future use
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Create comprehensive metadata for API documentation
    metadata = {
        'model_info': {
            'type': 'RandomForestClassifier',
            'version': '1.0',
            'training_date': '2025-05-23',
            'sklearn_version': '1.3.0'
        },
        'data_info': {
            'n_features': 4,
            'n_samples': 2000,
            'feature_range': [0, 10],
            'classes': [0, 1],
            'class_names': ['Class 0', 'Class 1']
        },
        'performance': {
            'train_accuracy': float(train_accuracy),
            'test_accuracy': float(test_accuracy),
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        },
        'feature_importance': feature_importance,
        'input_specifications': {
            'feature_1': {'min': 0, 'max': 10, 'description': 'Numeric feature 1'},
            'feature_2': {'min': 0, 'max': 10, 'description': 'Numeric feature 2'},
            'feature_3': {'min': 0, 'max': 10, 'description': 'Numeric feature 3'},
            'feature_4': {'min': 0, 'max': 10, 'description': 'Numeric feature 4'}
        },
        'test_predictions': predictions_summary,
        'usage_examples': [
            {'input': [5, 5, 5, 5], 'description': 'Middle-range values'},
            {'input': [2, 8, 3, 7], 'description': 'Mixed values'},
            {'input': [9, 1, 6, 4], 'description': 'Varied pattern'}
        ]
    }
    
    # Save metadata as JSON
    with open('model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ User-friendly model training completed!")
    print(f"   📊 Test accuracy: {test_accuracy:.4f}")
    print(f"   📁 Files created:")
    print(f"      - model.pkl (trained model)")
    print(f"      - scaler.pkl (feature scaler)")
    print(f"      - model_metadata.json (documentation)")
    print(f"   🎯 Input range: 0-10 for all features")
    print(f"   🎲 Output: Binary (0 or 1)")
    
    return model, metadata

# Test the saved model
def test_saved_model():
    """Test the saved model with user-friendly inputs"""
    print("\n=== Testing Saved Model ===")
    
    # Load the saved model
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Test with easy-to-understand values
    test_cases = [
        [0, 0, 0, 0],      # Minimum values
        [10, 10, 10, 10],  # Maximum values
        [5, 5, 5, 5],      # Middle values
        [1, 2, 8, 9],      # Mixed values
    ]
    
    for test_input in test_cases:
        prediction = model.predict([test_input])[0]
        probabilities = model.predict_proba([test_input])[0]
        confidence = probabilities.max()
        
        print(f"Input: {test_input} → Prediction: {prediction} (confidence: {confidence:.3f})")

if __name__ == "__main__":
    # Train the model
    model, metadata = train_user_friendly_model()
    
    # Test the saved model
    test_saved_model()
    
    print("\n🎉 Complete! Your model is ready for the frontend!")
    print("   Frontend users can now input values from 0-10")
    print("   Model will predict 0 or 1 with high confidence")