# =============================
# AI Study Planner + Performance Predictor
# Modern Dashboard Style with Gradient Background
# =============================

import sys
import os
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Load custom CSS
# -----------------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css(os.path.join(os.path.dirname(__file__), "style.css"))

# -----------------------------
# Fix imports dynamically
# -----------------------------
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from src.predict import predict_performance
except ModuleNotFoundError:
    st.error("❌ Could not import prediction module. Make sure 'src/' folder exists and contains predict.py")
    st.stop()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Sidebar: User Inputs
# -----------------------------
st.sidebar.header("📊 Enter Your Daily Routine")
st.sidebar.markdown("Adjust the sliders according to your daily habits:")

study_hours = st.sidebar.slider("Study Hours (per day)", 1, 10, 4)
sleep_hours = st.sidebar.slider("Sleep Hours (per day)", 1, 10, 7)
revision_freq = st.sidebar.slider("Revision Frequency (per week)", 0, 7, 2)
mock_score = st.sidebar.slider("Mock Test Score", 0, 100, 60)
screen_time = st.sidebar.slider("Screen Time (hrs per day)", 0, 10, 3)
break_time = st.sidebar.slider("Break Time (hrs per day)", 0, 5, 1)

input_data = [study_hours, sleep_hours, revision_freq, mock_score, screen_time, break_time]

# -----------------------------
# Main Title
# -----------------------------
st.title("📚 AI Study Planner + Performance Predictor")
st.markdown("""
Welcome! Adjust your daily habits in the **sidebar**, then click **Predict** 
to get your predicted exam score, risk level, and personalized study plan.
""")
st.markdown("---")

# -----------------------------
# Predict Button
# -----------------------------
if st.button("Predict Performance"):

    try:
        score, risk, plan = predict_performance(input_data)

        # -----------------------------
        # Cards Layout: Score, Risk, Study Plan
        # -----------------------------
        col1, col2, col3 = st.columns([1,1,2])

        with col1:
            st.subheader("🎯 Predicted Score")
            if score is not None:
                st.metric(label="Score", value=f"{score} / 100")
            else:
                st.warning("Could not predict score")

        with col2:
            st.subheader("⚠ Risk Level")
            if risk == "High":
                st.error(risk)
            elif risk == "Medium":
                st.warning(risk)
            else:
                st.success(risk)

        with col3:
            st.subheader("📝 Personalized Study Plan")
            st.info(plan)

        st.markdown("---")

        # -----------------------------
        # Tabs for Charts and Tips
        # -----------------------------
        tabs = st.tabs(["📊 Feature Impact", "💡 Tips & Suggestions"])

        # Feature Impact Tab
        with tabs[0]:
            features = ["Study Hours","Sleep Hours","Revision","Mock Score","Screen Time","Break Time"]
            values = [study_hours, sleep_hours, revision_freq, mock_score, screen_time, break_time]

            fig, ax = plt.subplots(figsize=(8,4))
            sns.barplot(x=values, y=features, palette="viridis", orient="h", ax=ax)
            ax.set_xlabel("Value")
            ax.set_ylabel("Feature")
            ax.set_title("Your Inputs vs Features")
            st.pyplot(fig)

        # Tips Tab
        with tabs[1]:
            st.markdown("""
- ⏰ Increase study hours gradually if low.
- 💤 Ensure sufficient sleep to retain memory.
- 🔁 Revise consistently (daily/weekly).
- 📝 Take mock tests and review mistakes.
- 📵 Reduce unnecessary screen time.
- ☕ Take short breaks to refresh focus.
""")

    except Exception as e:
        st.error(f"❌ Error predicting performance: {e}")
        st.stop()