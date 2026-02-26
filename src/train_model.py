# =============================
# AI Study Planner - Train Models
# =============================

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
import os

# -----------------------------
# 1️⃣ Ensure models folder exists
# -----------------------------
if not os.path.exists("../models"):
    os.makedirs("../models")

# -----------------------------
# 2️⃣ Load processed data
# -----------------------------
data_path = "../data/processed/clean_study_data.csv"
df = pd.read_csv(data_path)

# -----------------------------
# 3️⃣ Create risk level for classification
# -----------------------------
def risk_level(score):
    if score < 50:
        return "High"
    elif score < 70:
        return "Medium"
    else:
        return "Low"

df['risk_level'] = df['exam_score'].apply(risk_level)

# Encode risk level
le = LabelEncoder()
df['risk_level_encoded'] = le.fit_transform(df['risk_level'])

# -----------------------------
# 4️⃣ Features and targets
# -----------------------------
X = df[['study_hours','sleep_hours','revision_freq','mock_score','screen_time','break_time']]
y_reg = df['exam_score']
y_clf = df['risk_level_encoded']

# -----------------------------
# 5️⃣ Split data
# -----------------------------
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X, y_reg, test_size=0.2, random_state=42)
X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(X, y_clf, test_size=0.2, random_state=42)

# -----------------------------
# 6️⃣ Train regression model
# -----------------------------
reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
reg_model.fit(X_train_reg, y_train_reg)
y_pred_reg = reg_model.predict(X_test_reg)

print("✅ Regression Model Trained")
print("R2 Score:", r2_score(y_test_reg, y_pred_reg))
print("RMSE:", np.sqrt(mean_squared_error(y_test_reg, y_pred_reg)))

# Save regression model
pickle.dump(reg_model, open("../models/regression_model.pkl", "wb"))

# -----------------------------
# 7️⃣ Train classification model
# -----------------------------
clf_model = RandomForestClassifier(n_estimators=100, random_state=42)
clf_model.fit(X_train_clf, y_train_clf)
y_pred_clf = clf_model.predict(X_test_clf)

print("✅ Classification Model Trained")
print("Accuracy:", accuracy_score(y_test_clf, y_pred_clf))
print(classification_report(y_test_clf, y_pred_clf, target_names=le.classes_))

# Save classification model and label encoder
pickle.dump(clf_model, open("../models/classification_model.pkl", "wb"))
pickle.dump(le, open("../models/label_encoder.pkl", "wb"))

print("✅ All models saved in 'models/' folder")