import streamlit as st
import joblib
import pandas as pd

# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .title-container {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .title-container h1 {
        color: #1f2937;
        font-weight: 800;
        margin-bottom: 0;
    }
    .title-container p {
        color: #6b7280;
        font-size: 1.05rem;
        margin-top: 0.3rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #4f46e5, #6366f1);
        color: white;
        font-weight: 600;
        font-size: 1.05rem;
        padding: 0.7rem 0;
        border-radius: 10px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #4338ca, #4f46e5);
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(79, 70, 229, 0.35);
    }
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        text-align: center;
        margin-top: 1.5rem;
        border-left: 6px solid #4f46e5;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        text-align: center;
    }
    section[data-testid="stSidebar"] {
        background-color: #1f2937;
    }
    section[data-testid="stSidebar"] * {
        color: #f3f4f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Load Model
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load('model.pkl')

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    model_error = str(e)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown("""
<div class="title-container">
    <h1>🎓 Student Performance Predictor</h1>
    <p>Enter student details below to get an AI-powered performance prediction</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# Sidebar - Info
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.write(
        "This tool uses a trained Machine Learning model to predict a "
        "student's academic performance based on attendance, assignments, "
        "study habits, and other factors."
    )
    st.markdown("---")
    st.markdown("### 📌 How to use")
    st.write(
        "1. Adjust the sliders/dropdowns\n"
        "2. Click **Predict**\n"
        "3. View the predicted result"
    )
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit")

# ---------------------------------------------------------
# Input Form (Organized in Sections with Columns)
# ---------------------------------------------------------
st.markdown("### 📋 Student Details")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("#### 📊 Academic Metrics")
    attendance = st.slider("Attendance %", 0, 100, 75, help="Overall class attendance percentage")
    assignment = st.slider("Assignment Score", 0, 100, 70)
    internal = st.slider("Internal Assessment Score", 0, 100, 65)
    final_exam = st.slider("Final Exam Score", 0, 100, 60)

with col2:
    st.markdown("#### 🧑‍🎓 Personal & Behavioral Factors")
    study_hours = st.slider("Study Hours per Week", 0, 40, 10)
    gpa = st.slider("Previous Semester GPA", 0.0, 10.0, 7.0, step=0.1)
    extracurricular = st.selectbox("Extracurricular Participation", ["No", "Yes"])
    part_time_job = st.selectbox("Part-time Job", ["No", "Yes"])

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Quick Overview Metrics
# ---------------------------------------------------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("Attendance", f"{attendance}%")
m2.metric("Study Hours/Week", f"{study_hours} hrs")
m3.metric("Previous GPA", f"{gpa}")
m4.metric("Final Exam", f"{final_exam}%")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Predict Button + Result
# ---------------------------------------------------------
predict_col = st.columns([1, 2, 1])[1]
with predict_col:
    predict_clicked = st.button("🔮 Predict Performance")

if predict_clicked:
    if not model_loaded:
        st.error(f"⚠️ Could not load model.pkl: {model_error}")
    else:
        data = pd.DataFrame([[
            attendance, assignment, internal, study_hours, gpa,
            1 if extracurricular == "Yes" else 0,
            1 if part_time_job == "Yes" else 0,
            final_exam
        ]], columns=['attendance_percentage', 'assignment_score', 'internal_assessment_score',
                     'study_hours_per_week', 'previous_semester_gpa',
                     'extracurricular_participation', 'part_time_job', 'final_exam_score'])

        with st.spinner("Analyzing student data..."):
            result = model.predict(data)[0]

        # -----------------------------------------------------
        # Convert result to a 0-100 scale score for easy reading
        # -----------------------------------------------------
        try:
            score = float(result)
        except (ValueError, TypeError):
            score = None

        if score is not None:
            # Clamp score to 0-100 range for the visual scale
            score_clamped = max(0, min(100, score))

            # Determine performance category, color and emoji
            if score_clamped < 40:
                label, color, emoji = "Needs Improvement", "#ef4444", "😟"
            elif score_clamped < 60:
                label, color, emoji = "Average", "#f59e0b", "😐"
            elif score_clamped < 80:
                label, color, emoji = "Good", "#3b82f6", "🙂"
            else:
                label, color, emoji = "Excellent", "#22c55e", "🤩"

            st.markdown(f"""
            <div class="result-card">
                <h3 style="color:#6b7280; margin-bottom:0.3rem;">Predicted Performance</h3>
                <h1 style="color:{color}; font-size:2.8rem; margin:0.2rem 0;">{score_clamped:.1f} / 100</h1>
                <p style="font-size:1.3rem; font-weight:600; color:{color}; margin:0.3rem 0 1.2rem 0;">
                    {emoji} {label}
                </p>
                <div style="background:#e5e7eb; border-radius:10px; height:18px; width:100%; position:relative; overflow:hidden;">
                    <div style="background:linear-gradient(90deg,#ef4444,#f59e0b,#3b82f6,#22c55e);
                                height:100%; width:100%; opacity:0.35; position:absolute;"></div>
                    <div style="background:{color}; height:100%; width:{score_clamped}%;
                                border-radius:10px; position:relative; transition: width 0.6s ease;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#6b7280; margin-top:0.4rem;">
                    <span>0</span>
                    <span>25</span>
                    <span>50</span>
                    <span>75</span>
                    <span>100</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Simple progress bar as an additional, accessible indicator
            st.progress(int(score_clamped) / 100)
        else:
            # Fallback for non-numeric / categorical predictions (e.g. "Pass", "Fail")
            st.markdown(f"""
            <div class="result-card">
                <h3 style="color:#6b7280; margin-bottom:0.3rem;">Predicted Performance</h3>
                <h1 style="color:#4f46e5; font-size:2.5rem; margin-top:0;">{result}</h1>
            </div>
            """, unsafe_allow_html=True)

        st.balloons()