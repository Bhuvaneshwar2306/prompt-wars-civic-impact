import streamlit as st
import sys
import os
import streamlit as st
import backend_engine as backend

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import backend_engine as backend

st.title("🔍 Accountability System Tracking Module")
search_id = st.text_input("Provide your system Ticket reference ID code:")

if search_id:
    current_records = backend.load_data()
    match_found = next((r for r in current_records if r["id"].strip().upper() == search_id.strip().upper()), None)
            
    if match_found:
        st.success("Target Record Reference Located in System Storage Ledger!")
        col_t1, col_t2 = st.columns(2)
        col_t1.metric("Live Action Phase State", match_found["status"])
        col_t2.metric("Evaluated Hazard Urgency Level", match_found["priority"])
        st.info(f"💡 **AI Processing Accountability Tracker Statement:** {match_found['reasoning']}")
        if match_found["is_duplicate"]:
            st.warning(f"Note: This duplicate log was merged under primary master task asset index: {match_found['duplicate_of']}")
    else:
        st.error("Provided structural identifier does not match active municipal records.")
