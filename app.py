import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

CSV_FILE = "students.csv"

if not os.path.exists(CSV_FILE):
    print("students.csv not found. Creating sample data...")
    rng = np.random.default_rng(42)
    n = 200
    df = pd.DataFrame({
        "study_hours": rng.uniform(0, 10, n),
        "attendance": rng.uniform(50, 100, n),
        "previous_score": rng.uniform(35, 95, n),
        "assignments_done": rng.integers(0, 11, n),
    })
    df["final_score"] = (
        3 * df["study_hours"]
        + 0.2 * df["attendance"]
        + 0.4 * df["previous_score"]
        + 1.5 * df["assignments_done"]
        + rng.normal(0, 4, n)
    ).clip(0, 100)
    df.to_csv(CSV_FILE, index=False)
else:
    df = pd.read_csv(CSV_FILE)

print("Data loaded:", df.shape[0], "students")
print(df.head())

X = df.drop(columns=["final_score"])
y = df["final_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)
print("\nR2 score:", round(r2_score(y_test, pred), 3))
print("Average error (marks):", round(mean_absolute_error(y_test, pred), 2))

print("\n--- Predict a new student ---")
study = float(input("Study hours per day (0-10): "))
att = float(input("Attendance % : "))
prev = float(input("Previous exam score : "))
assign = int(input("Assignments done (0-10): "))

new_student = pd.DataFrame(
    [[study, att, prev, assign]], columns=X.columns
)
result = model.predict(new_student)[0]
print("\nPredicted final score:", round(min(max(result, 0), 100), 1))