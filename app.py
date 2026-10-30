import streamlit as st
import sys
import os

# --- CRITICAL HACKATHON PATH FIXER ---
# This forces Python to look inside the main folder regardless of what page is active
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import backend_engine as backend

# ==============================================================================
# MAIN PAGE ENTRY ROUTING LAYER
# ==============================================================================
st.set_page_config(
    page_title="Civic Impact Portal", 
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# STAGE 0: Execute immediate automated ledger seeding if storage is empty
backend.seed_database_if_empty()

# --- HERO HEADER PANEL ---
st.title("🏙️ Welcome to the From Complaints to Action Platform")
st.markdown("## PromptWars x ASTRA | Advanced Multi-Page Architectural Framework")
st.write("---")

st.info("👈 **TRANSITION THROUGH THE LIFECYCLE:** Use the sidebar menu on the left to seamlessly navigate between consumer intake terminals and administrative monitoring boards.")

# --- ARCHITECTURAL COMPONENT OVERVIEW GRID ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📝 Stage 1 & 2: Citizen Ingestion")
    st.write(
        "A fast, mobile-optimized capture terminal allowing citizens to log infrastructure "
        "defects under a minute with location logging. Integrated with our live AI prompt "
        "understanding client pipeline."
    )

with col2:
    st.markdown("### 📊 Stage 3 & 4: Operations Center")
    st.write(
        "An advanced analytics dashboard compiling active tickets, rendering interactive map "
        "hotspots via Pandas aggregations, and serving up an actionable priority workflow queue "
        "for field maintenance crews."
    )

with col3:
    st.markdown("### 🔍 Closed-Loop Verification")
    st.write(
        "A dedicated progress tracking lookup application that gives citizens instant tracking status "
        "transparency, displaying live workflow states read directly from our data layer."
    )

st.write("---")
st.caption("Developed for PromptWars 2026 | Built with Streamlit, Pandas, and OpenAI API Pipeline Layers.")
