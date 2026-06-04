import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
# from sklearn.neural_network import MLPClassifier  # Uncomment if you want to try MLP
from sklearn.metrics import accuracy_score
import joblib

# ✅ Step 1: Read CSV
data = pd.read_csv("data/game_history.csv")

# ✅ Step 2: Preprocessing
# Convert action (chaal, pack, show) into numbers
action_map = {"chaal": 0, "pack": 1, "show": 2}
data["action_encoded"] = data["action"].map(action_map)

# Features and Target
X = data[["card_strength", "pot", "player_coin", "opponent_coin"]]
y = data["action_encoded"]

# ✅ Step 3: Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Step 4: Train Model
model = DecisionTreeClassifier()
# model = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000)  # Optional

model.fit(X_train, y_train)

# ✅ Step 5: Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# ✅ Step 6: Save the model
joblib.dump(model, "ai_model/teen_patti_ai_model.joblib")
print("Model saved to ai_model/teen_patti_ai_model.joblib")
