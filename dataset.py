import pandas as pd
import random

data = []

for _ in range(200):

    n = random.randint(3, 10)

    burst = [random.randint(1, 10) for _ in range(n)]
    arrival = [random.randint(0, 5) for _ in range(n)]
    priority = [random.randint(1, 5) for _ in range(n)]

    avg_burst = sum(burst) / n
    avg_arrival = sum(arrival) / n
    priority_var = max(priority) - min(priority)

    # -------- LABEL LOGIC --------
    if avg_burst < 4:
        best = "SJF"
    elif priority_var > 2:
        best = "Priority"
    elif n > 6:
        best = "RR"
    else:
        best = "FCFS"

    data.append([n, avg_burst, avg_arrival, priority_var, best])

# -------- CREATE DATAFRAME --------
df = pd.DataFrame(data, columns=[
    "n",
    "avg_burst",
    "avg_arrival",
    "priority_var",
    "best"
])

# -------- SAVE FILE --------
df.to_csv("dataset.csv", index=False)

print("✅ dataset.csv created successfully!")