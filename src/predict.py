# src/predict.py

import pickle
import numpy as np
import os
from .planner import generate_plan  # RELATIVE IMPORT fixed

# -----------------------------
# 1️⃣ Paths to models
# -----------------------------
REG_MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/regression_model.pkl")
CLF_MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/classification_model.pkl")
LE_PATH = os.path.join(os.path.dirname(__file__), "../models/label_encoder.pkl")

# -----------------------------
# 2️⃣ Load models
# -----------------------------
try:
    reg_model = pickle.load(open(REG_MODEL_PATH, "rb"))
    clf_model = pickle.load(open(CLF_MODEL_PATH, "rb"))
    le = pickle.load(open(LE_PATH, "rb"))
except FileNotFoundError as e:
    print(f"Model file not found: {e}")
    print("⚠ Please run 'train_model.py' first to generate models.")
    raise e

# -----------------------------
# 3️⃣ Prediction function
# -----------------------------
def predict_performance(input_data):
    """
    Predict exam score, risk level, and generate study plan.

    Parameters:
    - input_data: List of [study_hours, sleep_hours, revision_freq, mock_score, screen_time, break_time]

    Returns:
    - score (float)
    - risk (str)
    - plan (str)
    """
    try:
        data = np.array(input_data).reshape(1, -1)

        # Predict exam score
        score = reg_model.predict(data)[0]

        # Predict risk level
        risk_encoded = clf_model.predict(data)[0]
        risk = le.inverse_transform([risk_encoded])[0]

        # Generate study plan
        plan = generate_plan(score, risk)

        return round(score, 2), risk, plan

    except Exception as e:
        print(f"Error in prediction: {e}")
        return None, None, f"Error: {e}"

# -----------------------------
# 4️⃣ Optional test when running directly
# -----------------------------
if __name__ == "__main__":
    sample_input = [5, 7, 3, 65, 3, 1]  # Example input
    score, risk, plan = predict_performance(sample_input)
    print("Predicted Score:", score)
    print("Risk Level:", risk)
    print("Study Plan:", plan)