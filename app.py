
import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pandas as pd
from PIL import Image
import json

# Premium Page Configuration
st.set_page_config(
    page_title="MedBTR CommandCenter Pro", 
    page_icon="🩺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Cyber Graphics Style Sheet
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top left, #0B132B 0%, #010409 100%) !important; 
        color: #E2E8F0 !important; 
    }
    h1 { 
        color: #38BDF8 !important; 
        font-family: 'Inter', sans-serif; 
        font-weight: 800 !important; 
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }
    h2, h3 { color: #06B6D4 !important; font-family: 'Inter', sans-serif; }
    div[data-testid="stForm"], div.stBlock, .stTabs {
        background: rgba(30, 41, 59, 0.45) !important;
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(12px) !important;
    }
    section[data-testid="stSidebar"] { 
        background-color: #0F172A !important; 
        border-right: 2px solid rgba(6, 180, 212, 0.2); 
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #020617 !important;
        color: #38BDF8 !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ MED-BTR COMMAND CENTER")
st.markdown("<p style='color: #94A3B8;'>19 MBBS Subjects • Daily Tracker • AI Ingestion Neural Engine</p>", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.markdown("### 🧬 SECURE AI CORE")
api_key = st.sidebar.text_input("Gemini Neural API Key:", type="password")

model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.sidebar.success("🔗 AI Core Linked Successfully")
    except Exception as api_err:
        st.sidebar.error("⚠️ Encryption Sync Failed.")
else:
    st.sidebar.info("📡 System Offline: Enter API Key to activate AI.")

# Initialize Session Data Safely
if 'daily_logs' not in st.session_state:
    st.session_state.daily_logs = {}
if 'study_metrics' not in st.session_state:
    st.session_state.study_metrics = {}
if 'qbank_errors' not in st.session_state:
    st.session_state.qbank_errors = []

# --- CYBER TABS SYSTEM ---
tab1, tab2, tab3 = st.tabs(["🕒 24h CHRONO-AUDIT", "🎯 METRICS & ERROR INGESTION", "📊 MISSION DIAGNOSTICS"])

# ==================== TAB 1: TIME AUDIT ====================
with tab1:
    st.markdown("### 🕒 Chronological Log Grid (00:00 - 00:00)")
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
    if st.button("🧠 INITIALIZE TIME-LEAK DIAGNOSTIC"):
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
                    st.markdown("<div style='background: #020617; padding: 20px; border-left: 4px solid #06B6D4; border-radius: 8px;'>", unsafe_allow_html=True)
                    st.write(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)

# ==================== TAB 2: METRICS & ERROR INGESTION ====================
with tab2:
    st.markdown("### 🎯 Daily Progress Ingestion Matrix")
    metric_date = st.date_input("Select Ingestion Date:", datetime.today(), key="date_tab2").strftime("%Y-%m-%d")
    
    if metric_date not in st.session_state.study_metrics:
        st.session_state.study_metrics[metric_date] = {"btr_pages": 0, "q_solved": 0, "q_incorrect": 0}
        
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.session_state.study_metrics[metric_date]["btr_pages"] = st.number_input("📚 BTR Core Pages Read:", min_value=0, value=st.session_state.study_metrics[metric_date]["btr_pages"], key=f"p_{metric_date}")
    with col_m2:
        st.session_state.study_metrics[metric_date]["q_solved"] = st.number_input("📝 QBank Vectors Solved:", min_value=0, value=st.session_state.study_metrics[metric_date]["q_solved"], key=f"s_{metric_date}")
    with col_m3:
        st.session_state.study_metrics[metric_date]["q_incorrect"] = st.number_input("❌ Core Incorrect Count:", min_value=0, value=st.session_state.study_metrics[metric_date]["q_incorrect"], key=f"i_{metric_date}")
        
    st.markdown(f"<p style='color:#10B981;'>✓ Metrics saved for: {metric_date}</p>", unsafe_allow_html=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("### 🚀 Multimodal QBank Error Parser")
    uploaded_files = st.file_uploader("Drop Diagnostic Screenshots Here:", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="screenshots")
    
    if st.button("🧬 TRIGGER NEURAL ERROR MAPPING"):
        if not api_key or model is None:
            st.error("Operation Aborted: AI Engine Offline.")
        elif not uploaded_files:
            st.warning("Data Void: Drop question screenshots first.")
        else:
            with st.spinner("Parsing medical imagery..."):
                for uploaded_file in uploaded_files:
                    try:
                        image = Image.open(uploaded_file)
                        prompt = "Analyze this medical question screenshot. Extract core MBBS Subject, high-yield Topic, and core mistake. Output strictly as JSON like this: {'Subject': 'Pathology', 'Topic': 'Amyloidosis', 'Core_Mistake': 'stain error'}"
                        response = model.generate_content([prompt, image])
                        clean_text = response.text.strip().replace("```json", "").replace("```", "")
                        data = json.loads(clean_text)
                        data['Date'] = metric_date
                        st.session_state.qbank_errors.append(data)
                        st.toast(f"⚡ Mapped: {data['Subject']}")
                    except Exception as parse_err:
                        st.error("Parser Skip: Error processing screenshot.")
                st.success("Batch Sequence Complete!")

    if st.session_state.qbank_errors:
        st.markdown("#### 📋 Compiled Telemetry Database (Mistakes)")
        df_errors = pd.DataFrame(st.session_state.qbank_errors)
        st.dataframe(df_errors, use_container_width=True)

# ==================== TAB 3: DIAGNOSTICS ====================
with tab3:
    st.markdown("### 📊 High-Yield Executive Performance Metrics")
    report_type = st.selectbox("Select Range Vector:", ["Daily Summary", "Weekly Performance Report", "Monthly Analytics Diagnostic"])
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        generate_report = st.button("📈 COMPILE HIGH-YIELD INTELLIGENCE REPORT")
    with col_b2:
        if st.button("🗑️ FLUSH APPLICATION MEMORY"):
            st.session_state.daily_logs = {}
            st.session_state.study_metrics = {}
            st.session_state.qbank_errors = []
            st.rerun()

    if generate_report:
        if not api_key or model is None:
            st.error("Neural Sync Interrupted: Key Configuration Missing.")
        else:
            with st.spinner("Processing diagnostics..."):
                all_schedules = ""
                for d, slots in st.session_state.daily_logs.items():
                    all_schedules += f"\nDate: {d}\n" + "\n".join([f"{k}: {v}" for k, v in slots.items() if v.strip()])
                
                metrics_summary = ""
                if st.session_state.study_metrics:
                    metrics_summary = pd.DataFrame.from_dict(st.session_state.study_metrics, orient='index').to_string()

                qbank_summary = ""
                if st.session_state.qbank_errors:
                    qbank_summary = pd.DataFrame(st.session_state.qbank_errors).to_string(index=False)
                
                prompt = f"Create a tactical {report_type} for an MBBS student based on this data:\nNotes Pages & QBank:\n{metrics_summary}\n\nErrors:\n{qbank_summary}\n\nTime logs:\n{all_schedules}\n\nGive: 1. Pages velocity & QBank accuracy rate %, 2. Weakest subjects/topics cluster, 3. Strategic BTR review counter-attack plan."
