import streamlit as st
import backend_engine as backend

st.header("Stage 1 & 2: Log a New Infrastructure Incident")

with st.form("citizen_capture_form"):
    desc = st.text_area("Provide issue details (Landmarks, safety concerns, infrastructure condition):")
    c1, c2 = st.columns(2)
    with c1:
        lat_input = st.number_input("Latitude", value=12.9716, format="%.4f")
    with c2:
        lon_input = st.number_input("Longitude", value=77.5946, format="%.4f")
    st.file_uploader("Attach Photo (Optional)", type=["png", "jpg", "jpeg"])
    
    submitted = st.form_submit_button("Submit to AI Pipeline")
    
    if submitted and desc:
        with st.spinner("Processing full-stack data pipeline..."):
            ai_analysis = backend.run_ai_understanding_pipeline(desc)
            records = backend.load_data()
            
            is_dup = False
            parent_id = None
            for r in records:
                if abs(r["latitude"] - lat_input) < 0.001 and abs(r["longitude"] - lon_input) < 0.001 and r["category"] == ai_analysis["category"]:
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
                "reasoning": f"SYSTEM NOTICE: Duplicate position match detected. Linked to parent task {parent_id}." if is_dup else ai_analysis["reasoning"],
                "action_brief": ai_analysis["action_brief"],
                "latitude": lat_input,
                "longitude": lon_input,
                "status": "Submitted",
                "is_duplicate": is_dup,
                "duplicate_of": parent_id
            }
            
            records.append(new_ticket)
            backend.save_data(records)
            st.success(f"🎉 Ticket Registered Successfully: {new_id}")
            st.json(new_ticket)
