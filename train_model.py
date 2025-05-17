from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib


#Load the iris dataset
iris = load_iris()
X, y = iris.data, iris.target

model = RandomForestClassifier(n_estimators=100, random_state=42)
# Train the model
model.fit(X, y)
# Save the model
joblib.dump(model, 'model/iris_model.pkl')
print("✅ Model trained and saved!")

