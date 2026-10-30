import streamlit as st
import backend_engine as backend

st.header("Citizen Real-Time Ticket Tracking Terminal")
search_id = st.text_input("Enter your unique Ticket ID:")

if search_id:
    current_records = backend.load_data()
    match_found = next((r for r in current_records if r["id"].strip().upper() == search_id.strip().upper()), None)
            
    if match_found:
        st.success("Ticket Reference Identified!")
        col_t1, col_t2 = st.columns(2)
        col_t1.metric("Current Assignment Status", match_found["status"])
        col_t2.metric("Assigned Infrastructure Priority", match_found["priority"])
        st.info(f"💡 **AI Accountability Tracker Note:** {match_found['reasoning']}")
    else:
        st.error("Ticket reference ID not matching active database data entries.")
