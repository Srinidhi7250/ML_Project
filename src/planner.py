# src/planner.py

def generate_plan(score, risk=None):
    """
    Generate personalized study plan based on predicted exam score and risk level.
    """
    try:
        if risk is None:
            risk = "Low"  # default if risk not provided
        score = float(score)
        if risk == "High" or score < 50:
            return "⚠ High Risk: Study 6-7 hours daily, frequent revision, minimize screen time, short breaks every hour."
        elif risk == "Medium" or score < 70:
            return "Moderate Risk: Study 4-5 hours daily, practice 2-3 mock tests weekly, take regular breaks."
        else:
            return "Low Risk: Good performance! Study 2-3 hours daily, focus on weak areas, maintain regular revisions."
    except Exception as e:
        return f"Error generating plan: {e}"

# -----------------------------------
# Test block to run this file directly
# -----------------------------------
if __name__ == "__main__":
    print(generate_plan(45, "High"))
    print(generate_plan(65, "Medium"))
    print(generate_plan(85, "Low"))
    print(generate_plan(75))  # Risk not provided, should default to Low