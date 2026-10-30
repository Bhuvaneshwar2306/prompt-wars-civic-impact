import streamlit as st
import sys
import os
import streamlit as st
import backend_engine as backend

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import backend_engine as backend

# --- SAAS INTAKE STYLING OVERRIDES ---
st.markdown("""
    <style>
    .stApp { background-color: #0B0F19 !important; }
    
    /* Transforming the boring container card */
    div[data-testid="stForm"] {
        background: rgba(22, 27, 42, 0.8) !important;
        border: 1px solid rgba(0, 242, 254, 0.15) !important;
        border-radius: 20px !important;
        padding: 40px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    
    /* Formatting Text Area Fields */
    textarea, input {
        background-color: #0B0F19 !important;
        color: #F3F4F6 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
    }
    
    /* Modern Section Header */
    .form-title {
        color: #00F2FE !important;
        font-weight: 800;
        font-size: 2rem;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="form-title">📝 Stage 1 & 2: Incident Intake Terminal</div>', unsafe_allow_html=True)

with st.form("citizen_capture_form"):
    desc = st.text_area("What infrastructure asset anomaly requires operational attention?")
    c1, c2 = st.columns(2)
    with c1:
        lat_input = st.number_input("Target Location Latitude Mapping", value=12.9716, format="%.4f")
    with c2:
        lon_input = st.number_input("Target Location Longitude Mapping", value=77.5946, format="%.4f")
    st.file_uploader("Multi-Modal Image Capture Verification Matrix (Optional)", type=["png", "jpg", "jpeg"])
    
    submitted = st.form_submit_button("⚡ Run Full-Stack Processing Pipeline")
    
    if submitted and desc:
        with st.spinner("Processing full-stack engine metrics..."):
            ai_analysis = backend.run_ai_understanding_pipeline(desc)
            records = backend.load_data()
            
            is_dup = False
            parent_id = None
            for r in records:
                distance = backend.calculate_haversine_distance(lat_input, lon_input, r["latitude"], r["longitude"])
                if distance < 150 and r["category"] == ai_analysis["category"]:
                    is_dup = True
                    parent_id = r["id"]
                    break
            
            new_id = f"REP-{len(records) + 1001}"
            new_ticket = {
                "id": new_id,
                "description": desc,
                "category": ai_analysis["category"],
                "summary": ai_analysis["summary"],
                "priority": "Low" if is_dup else ai_analysis["priority"],
                "reasoning": f"SYSTEM INTELLIGENCE NOTICE: Merged via proximity loop. Linked to master case {parent_id}." if is_dup else ai_analysis["reasoning"],
                "action_brief": ai_analysis["action_brief"],
                "latitude": lat_input,
                "longitude": lon_input,
                "status": "Submitted",
                "is_duplicate": is_dup,
                "duplicate_of": parent_id
            }
            
            records.append(new_ticket)
            backend.save_data(records)
            st.success(f"🚀 Ingestion Matrix Complete! Ticket Registered: {new_id}")
            st.json(new_ticket)
