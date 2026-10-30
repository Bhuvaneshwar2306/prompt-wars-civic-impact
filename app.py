import streamlit as st
import sys
import os

# Ensure the root path is appended for internal modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import backend_engine as backend

# Configure page and explicitly hide the default Streamlit sidebar navigation
st.set_page_config(
    page_title="Civic Impact Nexus", 
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database synthetic data parameters
backend.seed_database_if_empty()

# Initialize session state configuration variable to track chosen navigation paths
if "active_view" not in st.session_state:
    st.session_state["active_view"] = "home"

# --- PREMIUM GLOBAL INTRUDER CSS THEME DESIGN (WORLD ISSUES) ---
st.markdown("""
    <style>
    /* HIDE NATIVE STREAMLIT SIDEBAR DRAWER AND BUTTONS COMPLETELY */
    [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    
    /* Premium World Issue / Dark Infrastructure Mesh Network Backdrop */
    .stApp {
        background-color: #070913 !important;
        background-image: 
            radial-gradient(at 10% 20%, rgba(239, 68, 68, 0.04) 0px, transparent 40%),
            radial-gradient(at 90% 10%, rgba(0, 242, 254, 0.03) 0px, transparent 40%),
            radial-gradient(at 50% 80%, rgba(168, 85, 247, 0.03) 0px, transparent 50%) !important;
    }
    
    /* Modern Headline Styling */
    .nexus-title {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #FF4B4B 0%, #00F2FE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1.5px;
        margin-bottom: 0rem;
    }
    .nexus-subtitle {
        color: #9CA3AF !important;
        font-size: 1.25rem !important;
        font-weight: 400;
        margin-bottom: 2.5rem;
    }
    
    /* Glassmorphic Tactical Selector Cards */
    .selection-box {
        background: linear-gradient(145deg, rgba(20, 24, 39, 0.85) 0%, rgba(10, 13, 22, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
        text-align: center;
        margin-bottom: 20px;
    }
    .selection-box:hover {
        border-color: rgba(255, 75, 75, 0.4);
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(255, 75, 75, 0.1);
    }
    
    .icon-node { font-size: 3rem; margin-bottom: 15px; }
    .node-title {
        color: #FFFFFF !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        margin-bottom: 10px;
    }
    .node-desc {
        color: #9CA3AF !important;
        font-size: 0.95rem !important;
        line-height: 1.6;
        min-height: 80px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# ROUTER CONDITIONAL LOGIC CONTROL 
# ==============================================================================

if st.session_state["active_view"] == "home":
    st.markdown('<h1 class="nexus-title">🏙️ Civic Incident Nexus</h1>', unsafe_allow_html=True)
    st.markdown('<p class="nexus-subtitle">Global Infrastructure & Asset Anomaly Resolution Command Platform</p>', unsafe_allow_html=True)
    
    st.warning("⚠️ **SYSTEM OPERATIONAL OVERVIEW:** Select a module from the dashboard console below to deploy structural reporting forms, audit global telemetry maps, or execute ticket verification steps.")
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="selection-box">
                <div class="icon-node">📝</div>
                <div class="node-title">Citizen Intake Node</div>
                <div class="node-desc">Frictionless, rapid capture portal transforming raw text descriptions into prioritized, structured asset incidents instantly.</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open Intake Module", use_container_width=True, type="primary"):
            st.session_state["active_view"] = "citizen_form"
            st.rerun()
            
    with col2:
        st.markdown("""
            <div class="selection-box">
                <div class="icon-node">📊</div>
                <div class="node-title">Operations Command Deck</div>
                <div class="node-desc">Geospatial hotspot cluster radar monitoring system tracking urban asset failure patterns, duplicate submissions, and dispatch status parameters.</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Command Deck", use_container_width=True, type="primary"):
            st.session_state["active_view"] = "admin_dashboard"
            st.rerun()
            
    with col3:
        st.markdown("""
            <div class="selection-box">
                <div class="icon-node">🔍</div>
                <div class="node-title">Verification Terminal</div>
                <div class="node-desc">Closed-loop transparency registry database lookup tool allowing reporting citizens to track live resolution milestones via reference IDs.</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Access Tracking Line", use_container_width=True, type="primary"):
            st.session_state["active_view"] = "citizen_tracking"
            st.rerun()

# --- FIXED DYNAMIC PAGE EXECUTIONS (Bypasses Import Error) ---
elif st.session_state["active_view"] == "citizen_form":
    if st.button("⬅️ Return to Command Hub Menu"):
        st.session_state["active_view"] = "home"
        st.rerun()
    st.write("---")
    
    path = os.path.join("pages", "1_📝_Citizen_Form.py")
    with open(path, "r", encoding="utf-8") as file:
        exec(file.read(), globals())

elif st.session_state["active_view"] == "admin_dashboard":
    if st.button("⬅️ Return to Command Hub Menu"):
        st.session_state["active_view"] = "home"
        st.rerun()
    st.write("---")
    
    path = os.path.join("pages", "2_📊_Admin_Dashboard.py")
    with open(path, "r", encoding="utf-8") as file:
        exec(file.read(), globals())

elif st.session_state["active_view"] == "citizen_tracking":
    if st.button("⬅️ Return to Command Hub Menu"):
        st.session_state["active_view"] = "home"
        st.rerun()
    st.write("---")
    
    path = os.path.join("pages", "3_🔍_Citizen_Tracking.py")
    with open(path, "r", encoding="utf-8") as file:
        exec(file.read(), globals())
