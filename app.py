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

# Tagda Medical-Tech Cyber Graphics & Custom CSS Styling
st.markdown("""
    <style>
    /* Main Background with Deep Tech Gradient */
    .stApp { 
        background: radial-gradient(circle at top left, #0B132B 0%, #010409 100%) !important; 
        color: #E2E8F0 !important; 
    }
    
    /* Medical High-Tech Headers */
    h1 { 
        color: #38BDF8 !important; 
        font-family: 'Inter', sans-serif; 
        font-weight: 800 !important; 
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
        letter-spacing: -0.5px;
    }
    h2, h3 { 
        color: #06B6D4 !important; 
        font-family: 'Inter', sans-serif; 
        font-weight: 700 !important; 
    }
    
    /* Glassmorphism Premium Grid Cards for Inputs */
    div[data-testid="stForm"], div.stBlock, .stTabs {
        background: rgba(30, 41, 59, 0.45) !important;
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Cyber Sidebar styling */
    section[data-testid="stSidebar"] { 
        background-color: #0F172A !important; 
        border-right: 2px solid rgba(6, 180, 212, 0.2); 
    }
    
    /* Glow effect on Text inputs & Numeric fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #020617 !important;
        color: #38BDF8 !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus { 
        border-color: #06B6D4 !important; 
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.5) !important;
    }
    
    /* Premium Futuristic Gradient Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.6) !important;
    }
    
    /* Customized Neon Tabs Selector */
    button[data-baseweb="tab"] { 
        font-size: 16px !important; 
        color: #64748B !important; 
        font-weight: 600; 
        padding: 12px 20px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] { 
        color: #38BDF8 !important; 
        font-weight: 800; 
        border-bottom: 3px solid #38BDF8 !important;
    }
    
    /* Custom Stat Card Look */
    .metric-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px dashed rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Main Banner Accent
st.markdown("<div style='border-left: 5px solid #06B6D4; padding-left: 15px; margin-bottom: 20px;'>", unsafe_allow_html=True)
st.title("⚡ MED-BTR COMMAND CENTER")
st.markdown("<p style='color: #94A3B8; font-size: 1.15rem; font-weight: 500;'>19 MBBS Subjects Smart Execution Rig • Precision Time Audit • AI Error Neural Engine</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- SIDEBAR: CONTROL PANEL ---
st.sidebar.markdown("<h2 style='font-size: 1.5rem; color: #38BDF8 !important;'>🧬 SECURE CORE</h2>", unsafe_allow_html=True)
api_key = st.sidebar.text_input("Gemini Neural API Key:", type="password", help="Generate keys safely via Google AI Studio")

model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.sidebar.success("🔗 AI Core Linked Successfully")
    except Exception as e:
        st.sidebar.error("⚠️ Encryption Sync Failed: Invalid Key Format.")
else:
    st.sidebar.info("📡 System Offline: Mount Gemini API Key to activate AI Diagnostics.")

# Persistent Storage Mechanics
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
            with st.spinner("Decoding timeline anomalies..."):
                schedule_text = "\n".join([f"{k}: {v}" for k, v in st.session_state.daily_logs[selected_date].items() if v.strip()])
                if not schedule_text.strip():
                    st.warning("Data Void: Log at least a few hourly vectors before execution.")
                else:
                    prompt = f"Analyze this elite medical student's hourly schedule for MBBS 19 subjects preparation. Be brutal, highly direct, point out exactly where they leaked time, and provide a 3-bullet hyper-efficient roadmap for tomorrow.\n\nTimeline:\n{schedule_text}"
                    try:
                        response = model.generate_content(prompt)
                        st.markdown("<div style='background: linear-gradient(135deg, rgba(30,41,59,0.9) 0%, rgba(15,23,42,0.9) 100%); padding: 20px; border-left: 4px solid #06B6D4; border-radius: 8px;'>", unsafe_allow_html=True)
                        st.markdown("#### ⚡ AI Optimization Log:")
                        st.write(response.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Execution Error: {e}")

# ==================== TAB 2: METRICS & ERROR INGESTION ====================
with tab2:
    st.markdown("### 🎯 Daily Quantifiable Ingestion Matrix")
    metric_date = st.date_input("Select Ingestion Date:", datetime.today(), key="date_tab2").strftime("%Y-%m-%d")
    
    if metric_date not in st.session_state.study_metrics:
        st.session_state.study_metrics[metric_date] = {"btr_pages": 0, "q_solved": 0, "q_incorrect": 0}
        
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.session_state.study_metrics[metric_date]["btr_pages"] = st.number_input("📚 BTR Core Pages Read:", min_value=0, value=st.session_state.study_metrics[metric_date]["btr_pages"], key=f"pages_{metric_date}")
    with col_m2:
        st.session_state.study_metrics[metric_date]["q_solved"] = st.number_input("📝 QBank Vectors Solved:", min_value=0, value=st.session_state.study_metrics[metric_date]["q_solved"], key=f"solved_{metric_date}")
    with col_m3:
        st.session_state.study_metrics[metric_date]["q_incorrect"] = st.number_input("❌ Core Incorrect Count:", min_value=0, value=st.session_state.study_metrics[metric_date]["q_incorrect"], key=f"incorrect_{metric_date}")
        
    st.markdown(f"<p style='color:#10B981; font-weight:600;'>✓ System Updated for Vectors: {metric_date}</p>", unsafe_allow_html=True)

    st.markdown("<br><hr style='border: 1px solid rgba(56, 189, 248, 0.15);'><br>", unsafe_allow_html=True)
    st.markdown("### 🚀 Multimodal QBank Error Parser")
    st.write("Feed screenshot vectors of incorrect questions. Neural engine will map concepts automatically.")
    
    uploaded_files = st.file_uploader("Drop Diagnostic Screenshots Here:", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="screenshots")
    
    if st.button("🧬 TRIGGER NEURAL ERROR MAPPING"):
        if not api_key or model is None:
            st.error("Operation Aborted: AI Engine Offline.")
        elif not uploaded_files:
            st.warning("Data Void: Drop clear question screenshots first.")
        else:
            with st.spinner("Parsing medical imagery and schemas..."):
                for uploaded_file in uploaded_files:
                    try:
                        image = Image.open(uploaded_file)
