import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pandas as pd
from PIL import Image
import json

# Premium Page Configuration for Mobile Devices
st.set_page_config(
    page_title="MedTracker Pro", 
    page_icon="🩺", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-Premium Custom Styling for Mobile Layout
st.markdown("""
    <style>
    .stApp { 
        background: #090B10 !important; 
        color: #A0AEC0 !important;
        font-family: 'Inter', sans-serif;
    }
    .app-header {
        padding: 5px 0px;
        margin-bottom: 20px;
    }
    .app-title {
        color: #38BDF8 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    .app-subtitle {
        color: #4A5568 !important;
        font-size: 0.85rem !important;
        margin-top: -3px;
    }
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-bottom: 20px;
    }
    .dashboard-card {
        background: #11141D !important;
        border: 1px solid #1E2330 !important;
        border-radius: 14px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .card-icon {
        font-size: 1.5rem;
        margin-bottom: 2px;
    }
    .card-value {
        font-size: 2rem;
        font-weight: 800;
        margin: 2px 0;
    }
    .card-value.blue { color: #6366F1; }
    .card-value.green { color: #10B981; }
    .card-value.cyan { color: #06B6D4; }
    .card-value.red { color: #EF4444; }
    .card-title {
        color: #4A5568;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .section-title {
        color: #E2E8F0 !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #11141D !important;
        color: #F8FAFC !important;
        border: 1px solid #1E2330 !important;
        border-radius: 12px !important;
    }
    label {
        color: #4A5568 !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
    }
    button[data-baseweb="tab"] { 
        font-size: 12px !important; 
        color: #4A5568 !important; 
        font-weight: 700;
    }
    button[data-baseweb="tab"][aria-selected="true"] { 
        color: #38BDF8 !important; 
        border-bottom-color: #38BDF8 !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Top Native Header Block
st.markdown("""
    <div class='app-header'>
        <div class='app-title'>🩺 MedTracker Pro</div>
        <div class='app-subtitle'>MBBS 19-Subject System • Daily Log + Reading + QBank + AI Reports</div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.markdown("### 🧬 SECURE AI CORE")
api_key = st.sidebar.text_input("Gemini Neural API Key:", type="password")

model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        st.sidebar.success("🔗 AI Core Linked Successfully")
    except Exception as e:
        st.sidebar.error("API configuration error.")
else:
    st.sidebar.info("📡 System Offline: Enter API Key to activate AI.")

# Initialize Session Data Safely
if 'daily_logs' not in st.session_state:
    st.session_state.daily_logs = {}
if 'study_metrics' not in st.session_state:
    st.session_state.study_metrics = {}
if 'qbank_errors' not in st.session_state:
    st.session_state.qbank_errors = []

# Raw Metrics Math
study_days_count = max(len(st.session_state.study_metrics), 1)
total_pages_accumulated = sum([v.get("btr_pages", 0) for v in st.session_state.study_metrics.values()])
total_qbank_sessions = sum([1 for v in st.session_state.study_metrics.values() if v.get("q_solved", 0) > 0])
total_wrong_answers = sum([v.get("q_incorrect", 0) for v in st.session_state.study_metrics.values()]) + len(st.session_state.qbank_errors)

# Native Navigation Tabs System
tab1, tab2, tab3 = st.tabs(["📆 Daily Log", "📚 Reading & QBank", "📊 Reports & Analytics"])

# ==================== TAB 1: DAILY LOG ====================
with tab1:
    st.markdown("<div class='section-title'>🕒 Chronological Log Grid (00:00 - 00:00)</div>", unsafe_allow_html=True)
    selected_date = st.date_input("Target Date Vector:", datetime.today(), key="date_tab1").strftime("%Y-%m-%d")
    
    if selected_date not in st.session_state.daily_logs:
        st.session_state.daily_logs[selected_date] = {f"{i:02d}:00 - {(i+1)%24:02d}:00": "" for i in range(24)}
    
    col1, col2 = st.columns(2)
    slots = list(st.session_state.daily_logs[selected_date].keys())
    
    for idx, slot in enumerate(slots):
        current_val = st.session_state.daily_logs[selected_date][slot]
        label = f"🌙 Late Night Shift ({slot})" if idx < 5 or idx >= 22 else f"☀️ Core Shift ({slot})"
        if idx < 12:
            with col1:
                st.session_state.daily_logs[selected_date][slot] = st.text_input(label, value=current_val, key=f"t_{selected_date}_{slot}")
        else:
            with col2:
                st.session_state.daily_logs[selected_date][slot] = st.text_input(label, value=current_val, key=f"t_{selected_date}_{slot}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🧠 INITIALIZE TIME-LEAK DIAGNOSTIC", key="btn_audit"):
        if not api_key or model is None:
            st.error("Operation Aborted: AI Neural Key Missing.")
        else:
            schedule_text = "\n".join([f"{k}: {v}" for k, v in st.session_state.daily_logs[selected_date].items() if v.strip()])
            if not schedule_text.strip():
                st.warning("Data Void: Log at least a few hourly vectors.")
            else:
                with st.spinner("Decoding timeline anomalies..."):
                    prompt = f"Analyze this medical student's schedule for MBBS prep. Point out time leaks and provide 3 actionable focus points.\n\nSchedule:\n{schedule_text}"
                    response = model.generate_content(prompt)
                    st.markdown("<div style='background: #11141D; padding: 20px; border-left: 4px solid #38BDF8; border-radius: 12px; color: #E2E8F0;'>", unsafe_allow_html=True)
                    st.write(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)

# ==================== TAB 2: READING & QBANK ENTRY ====================
with tab2:
    st.markdown("<div class='section-title'>➕ Reading Session Add Karo</div>", unsafe_allow_html=True)
    metric_date = st.date_input("Date", datetime.today(), key="date_tab2").strftime("%Y-%m-%d")
    
    subject = st.selectbox("Subject", ["Anatomy", "Physiology", "Biochemistry", "Pathology", "Microbiology", "Pharmacology", "Forensic Medicine", "Community Medicine", "ENT", "Ophthalmology", "Obstetrics & Gynecology", "Pediatrics", "Medicine", "Surgery", "Orthopedics", "Dermatology", "Psychiatry", "Radiology", "Anesthesia"])
    topic = st.text_input("Topic / Chapter", placeholder="e.g. Liver Anatomy, Krebs Cycle...")
    source_type = st.selectbox("Source Type", ["BTR Notes", "QBank", "Main Notes", "Video Lecture"])
    
    col_sub1, col_sub2, col_sub3 = st.columns(3)
    with col_sub1:
        pages_read = st.number_input("Pages Read", min_value=0, value=0)
    with col_sub2:
        from_page = st.number_input("From Page", min_value=0, value=0)
    with col_sub3:
        to_page = st.number_input("To Page", min_value=0, value=0)
        
    clarity = st.slider("Clarity Rating (1-5)", min_value=1, max_value=5, value=3)

    st.markdown("<br><div class='section-title'>📝 QBank Numerical Stats</div>", unsafe_allow_html=True)
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        q_solved = st.number_input("Total QBank Solved Today:", min_value=0, value=0)
    with col_q2:
        q_incorrect = st.number_input("Total Incorrect Questions Today:", min_value=0, value=0)

    if st.button("📖 Session Save Karo", key="btn_save_metrics"):
        if metric_date not in st.session_state.study_metrics:
            st.session_state.study_metrics[metric_date] = {"btr_pages": 0, "q_solved": 0, "q_incorrect": 0}
        
        st.session_state.study_metrics[metric_date]["btr_pages"] += pages_read
        st.session_state.study_metrics[metric_date]["q_solved"] += q_solved
        st.session_state.study_metrics[metric_date]["q_incorrect"] += q_incorrect
        st.success(f"✓ Metrics Saved successfully!")
        st.rerun()

    # --- HERE IS THE FIXED SCREENSHOT ERROR PARSER SECTION ---
    st.markdown("<br><hr style='border-color:#1E2330;'><br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🚀 Multimodal QBank Screenshot Error Parser</div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Drop Question Screenshots Here:", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="screenshots")
    
    # NEW FIXED BUTTON PLACEMENT BELOW THE FILE UPLOADER
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    if st.button("🧬 TRIGGER NEURAL ERROR MAPPING", key="btn_error_parse"):
        if not api_key or model is None:
            st.error("Operation Aborted: AI Engine Offline. Please add Gemini API Key.")
        elif not uploaded_files:
