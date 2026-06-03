import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pandas as pd
from PIL import Image
import json

# Premium Page Configuration
st.set_page_config(
    page_title="MedBTR Tracker Pro", 
    page_icon="🩺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Graphics & Custom CSS Styling
st.markdown("""
    <style>
    /* Background and global fonts */
    .stApp { background-color: #0F172A; color: #E2E8F0; }
    
    /* Main Headers */
    h1, h2, h3 { color: #38BDF8 !important; font-family: 'Inter', sans-serif; font-weight: 700; }
    
    /* Premium Cards for Inputs */
    div[data-testid="stForm"], div.stBlock {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #1E293B !important; border-right: 1px solid #334155; }
    
    /* Custom Styling for Time Slots Inputs */
    .stTextInput>div>div>input {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
    .stTextInput>div>div>input:focus { border-color: #38BDF8 !important; }
    
    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4) !important;
    }
    
    /* Tabs Customization */
    button[data-baseweb="tab"] { font-size: 16px !important; color: #94A3B8 !important; font-weight: 500; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #38BDF8 !important; font-weight: bold; border-bottom-color: #38BDF8 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 MedBTR Smart AI Tracker")
st.markdown("<p style='color: #94A3B8; font-size: 1.1rem;'>Optimize your 19 MBBS Subjects prep, audit hourly time leaks, and master high-yield QBank mistakes.</p>", unsafe_allow_html=True)

# --- SIDEBAR: API KEY & ROBUST STORAGE ---
st.sidebar.markdown("<h2 style='font-size: 1.5rem;'>🔑 Control Panel</h2>", unsafe_allow_html=True)
api_key = st.sidebar.text_input("Gemini API Key:", type="password", help="Get a free key from Google AI Studio")

# Crash Protection: Initialize safely
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.sidebar.error("Invalid API Key format.")
else:
    st.sidebar.info("💡 Pro Tip: Get a free API key from Google AI Studio to run this app completely free forever.")

if 'daily_logs' not in st.session_state:
    st.session_state.daily_logs = {}
if 'qbank_errors' not in st.session_state:
    st.session_state.qbank_errors = []

# --- TABS LAYOUT ---
tab1, tab2, tab3 = st.tabs(["🕒 24h Time Audit", "🎯 Smart QBank Analytics", "📊 Executive AI Reports"])

# ==================== TAB 1: 24h TIME AUDIT ====================
with tab1:
    st.markdown("### 🕒 24-Hour Micro-Tracker (00:00 to 00:00)")
    selected_date = st.date_input("Choose Tracking Date:", datetime.today()).strftime("%Y-%m-%d")
    
    if selected_date not in st.session_state.daily_logs:
        st.session_state.daily_logs[selected_date] = {f"{i:02d}:00 - {(i+1)%24:02d}:00": "" for i in range(24)}
    
    col1, col2 = st.columns(2)
    slots = list(st.session_state.daily_logs[selected_date].keys())
    
    for idx, slot in enumerate(slots):
        current_val = st.session_state.daily_logs[selected_date][slot]
        # Late night active styling anchor for MBBS night owls
        label = f"🌙 {slot}" if idx < 5 or idx >= 22 else f"☀️ {slot}"
        
        if idx < 12:
            with col1:
                st.session_state.daily_logs[selected_date][slot] = st.text_input(label, value=current_val, key=f"t_{selected_date}_{slot}")
        else:
            with col2:
                st.session_state.daily_logs[selected_date][slot] = st.text_input(label, value=current_val, key=f"t_{selected_date}_{slot}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🧠 Generate AI Efficiency Audit"):
        if not api_key:
            st.error("Please add your Gemini API Key in the sidebar.")
        else:
            with st.spinner("AI is auditing your day..."):
                schedule_text = "\n".join([f"{k}: {v}" for k, v in st.session_state.daily_logs[selected_date].items() if v.strip()])
                if not schedule_text.strip():
                    st.warning("Please fill your schedule entries first.")
                else:
                    prompt = f"Analyze this medical student's daily 24h schedule for MBBS/BTR preparation. Point out exactly where they can save time, track if they studied late night effectively, and give 3 bullet points on how to maximize focus tomorrow.\n\nSchedule:\n{schedule_text}"
                    try:
                        response = model.generate_content(prompt)
                        st.markdown("<div style='background-color: #1E293B; padding: 15px; border-left: 4px solid #38BDF8; border-radius: 4px;'>", unsafe_allow_html=True)
                        st.write(response.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"API Error: Please check your key or connection. Details: {e}")

# ==================== TAB 2: SMART QBANK ANALYTICS ====================
with tab2:
    st.markdown("### 🎯 AI Screenshot Error Mapping")
    st.write("Upload clear screenshots of incorrect QBank questions. The AI will parse them instantly.")
    
    q_date = st.date_input("QBank Session Date:", datetime.today()).strftime("%Y-%m-%d")
    uploaded_files = st.file_uploader("Upload Question Screenshots:", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("🚀 Auto-Extract Mistakes"):
        if not api_key:
            st.error("Please configure the Gemini API Key.")
        elif not uploaded_files:
            st.warning("No files uploaded.")
        else:
            with st.spinner("Processing medical images with multimodal AI..."):
                for uploaded_file in uploaded_files:
                    try:
                        image = Image.open(uploaded_file)
                        prompt = """Analyze this medical entrance exam question screenshot. Extract:
                        1. The core MBBS Subject (out of the 19 standard subjects).
                        2. The high-yield Topic/BTR concept.
                        3. The core mistake/educational pearl.
                        Provide ONLY a valid JSON object like this:
                        {"Subject": "Pathology", "Topic": "Amyloidosis", "Core_Mistake": "Confused Apple-green birefringence with Congo Red stain properties"}
                        Do not wrap it in markdown block fences."""
                        
                        response = model.generate_content([prompt, image])
                        clean_text = response.text.strip().replace("```json", "").replace("```", "")
                        data = json.loads(clean_text)
                        data['Date'] = q_date
                        st.session_state.qbank_errors.append(data)
                        st.toast(f"Successfully tracked: {data['Topic']}")
                    except Exception as e:
                        # Crash prevention loop fallback
                        st.error(f"Could not parse one of the screenshots. Ensuring app safety.")
                st.success("Batch execution completed!")

    if st.session_state.qbank_errors:
        st.markdown("#### 📋 Current Error Log Database")
        df_errors = pd.DataFrame(st.session_state.qbank_errors)
        st.dataframe(df_errors, use_container_width=True)

# ==================== TAB 3: EXECUTIVE AI REPORTS ====================
with tab3:
    st.markdown("### 📊 High-Yield Performance Dashboard")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        generate_report = st.button("📈 Compile Instant Progress Analytics Report")
    with col_b2:
        if st.button("🗑️ Reset Application Data"):
            st.session_state.daily_logs = {}
            st.session_state.qbank_errors = []
            st.rerun()

    if generate_report:
        if not api_key:
            st.error("API Key required.")
        else:
            with st.spinner("Generating deep high-yield diagnostic metrics..."):
                all_schedules = ""
                for date, slots in st.session_state.daily_logs.items():
                    all_schedules += f"\nDate: {date}\n" + "\n".join([f"{k}: {v}" for k, v in slots.items() if v.strip()])
                
                qbank_summary = ""
                if st.session_state.qbank_errors:
                    qbank_summary = pd.DataFrame(st.session_state.qbank_errors).to_string(index=False)
                
                prompt = f"You are an elite MBBS Academic Coach. Create a highly strategic work completion and mistakes analytic report.\n1. Identify the top 3 highest weak subjects/topics from the QBank error logs.\n2. Suggest exactly which Core BTR videos/tables to revise.\n3. Identify timeline inefficiencies.\n\nDATA:\nSchedules:\n{all_schedules}\n\nQBank Errors:\n{qbank_summary}"
                
                try:
                    response = model.generate_content(prompt)
                    st.markdown("---")
