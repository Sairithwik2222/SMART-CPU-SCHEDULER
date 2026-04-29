import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import os

# -------- AUTO CREATE DATASET --------
if not os.path.exists("dataset.csv"):
    import dataset  # creates dataset.csv

# -------- LOAD DATA --------
df = pd.read_csv("dataset.csv")

X = df[["n", "avg_burst", "avg_arrival", "priority_var"]]
y = df["best"]

# -------- MODELS --------
models = {
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "KNN": KNeighborsClassifier()
}

best_model = None
best_score = 0

# -------- TRAIN & SELECT BEST MODEL --------
for name, model in models.items():
    model.fit(X, y)
    score = model.score(X, y)
    print(name, "Accuracy:", score)

    if score > best_score:
        best_score = score
        best_model = model

# -------- PREDICT FUNCTION --------
def predict_best(processes):

    n = len(processes)
    avg_burst = sum(p['burst'] for p in processes) / n
    avg_arrival = sum(p['arrival'] for p in processes) / n
    priority_var = max(p['priority'] for p in processes) - min(p['priority'] for p in processes)

    features = [[n, avg_burst, avg_arrival, priority_var]]

    return best_model.predict(features)[0]