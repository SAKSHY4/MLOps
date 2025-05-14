# train_model.py - Create a simple ML model
import pickle
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Generate a simple dataset
X, y = make_classification(n_samples=1000, n_features=4, 
                          n_informative=2, n_redundant=0, 
                          random_state=42)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple model
model = RandomForestClassifier(n_estimators=10)
model.fit(X_train, y_train)

# Save the model to disk
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved as model.pkl")
print(f"Model accuracy: {model.score(X_test, y_test):.2f}")