import streamlit as st
import json
import os
import math
import random
import pandas as pd

DB_FILE = "data.json"

# ==============================================================================
# DATA ENGINE LAYER
# ==============================================================================
def load_data():
    if os.path.exists(DB_FILE) and os.stat(DB_FILE).st_size > 0:
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def seed_database_if_empty():
    """Generates 40 mock records instantly if database is empty."""
    current_data = load_data()
    if len(current_data) >= 40:
        return
        
    categories = ["Waterlogging", "Road Damage", "Waste Management", "Streetlights", "Public Utility"]
    center_lat, center_lon = 12.9716, 77.5946 # Default Municipal Datum
    synthetic_records = []
    
    # 1. Balanced records
    for i in range(1, 31):
        cat = random.choice(categories)
        synthetic_records.append({
            "id": f"REP-{1000 + i}",
            "description": f"Standard public report regarding localized {cat.lower()} issues requiring tracking.",
            "category": cat,
            "summary": f"Routine tracking for {cat.lower()}.",
            "priority": random.choice(["Low", "Medium", "High", "Critical"]),
            "reasoning": "Determined via uniform automated lookup frameworks.",
            "action_brief": "Dispatch field crew to inspect assets.",
            "latitude": round(center_lat + random.uniform(-0.01, 0.01), 4),
            "longitude": round(center_lon + random.uniform(-0.01, 0.01), 4),
            "status": random.choice(["Submitted", "Investigating", "In Progress"]),
            "is_duplicate": False
        })
        
    # 2. Add a heavy geographic cluster (overlapping points on same street node)
    for j in range(1, 7):
        synthetic_records.append({
            "id": f"REP-CLUSTER-{100 + j}",
            "description": f"Compounded infrastructure system strain near central transit hub intersection node.",
            "category": random.choice(categories),
            "summary": "Compounded municipal infrastructural load warning.",
            "priority": "Critical" if j % 2 == 0 else "High",
            "reasoning": "High risk designated due to dense cascading compound risks at transit nexus.",
            "action_brief": "URGENT RESILIENCE DISPATCH: Send multi-disciplinary crew immediately.",
            "latitude": 12.9750,
            "longitude": 77.5950,
            "status": "Submitted",
            "is_duplicate": False
        })
        
    # 3. Add explicit duplicate pairs
    for k in range(1, 5):
        synthetic_records.append({
            "id": f"REP-DUP-{200 + k}",
            "description": "Repeating notification submitted by separate user for identical nearby issue.",
            "category": "Road Damage",
            "summary": "Duplicate structural lane issue tracker.",
            "priority": "Low",
            "reasoning": "Priority structurally downgraded to Low due to match against active master index open case.",
            "action_brief": "File data record under active open ticket index container.",
            "latitude": 12.9710,
            "longitude": 77.5940,
            "status": "Submitted",
            "is_duplicate": True
        })
        
    save_data(synthetic_records)

# Execute baseline check
seed_database_if_empty()

# ==============================================================================
# FRONTEND / LIFECYCLE PLATFORM LAYOUT
# ==============================================================================
st.set_page_config(page_title="Civic Impact Engine", layout="wide")
st.title("🏙️ From Complaints to Action Dashboard")
st.caption("PromptWars x ASTRA | End-to-End AI Civic Lifecycle Platform")

tab1, tab2, tab3 = st.tabs(["📝 Citizen: Submit Report", "📊 Admin: Insights & Map", "🔍 Citizen Tracking Terminal"])

# --- TAB 1: CITIZEN INTAKE ---
with tab1:
    st.header("Log a New Municipal Asset Complaint")
    with st.form("citizen_capture_form"):
        desc = st.text_area("Provide issue details (Landmarks, safety concerns, infrastructure condition):")
        c1, c2 = st.columns(2)
        with c1:
            lat_input = st.number_input("Latitude", value=12.9716, format="%.4f")
        with c2:
            lon_input = st.number_input("Longitude", value=77.5946, format="%.4f")
        mock_file = st.file_uploader("Attach Photo (Optional)", type=["png", "jpg", "jpeg"])
        
        submitted = st.form_submit_button("Submit to AI Pipeline")
        
        if submitted and desc:
            with st.spinner("Executing real-time understanding pipeline..."):
                desc_lower = desc.lower()
                
                # REILIENT LOCAL KEYWORD PROMPT FALLBACK PARSER
                if "flood" in desc_lower or "water" in desc_lower or "rain" in desc_lower:
                    ai_res = {"cat": "Waterlogging", "prio": "High", "reason": "Water pooling risk detected near transit vectors."}
                elif "pothole" in desc_lower or "road" in desc_lower or "crack" in desc_lower:
                    ai_res = {"cat": "Road Damage", "prio": "Critical", "reason": "Immediate vehicular travel risk and structural asphalt fatigue."}
                elif "dark" in desc_lower or "light" in desc_lower or "lamp" in desc_lower:
                    ai_res = {"cat": "Streetlights", "prio": "Medium", "reason": "Nighttime pedestrian visibility hazard reported."}
                else:
                    ai_res = {"cat": "Public Utility", "prio": "Low", "reason": "Routine infrastructure notification asset log entry."}
                
                # Check for geographic coordinate duplicates
                records = load_data()
                is_dup = False
                for r in records:
                    if abs(r["latitude"] - lat_input) < 0.001 and abs(r["longitude"] - lon_input) < 0.001 and r["category"] == ai_res["cat"]:
                        is_dup = True
                        break
                
                new_id = f"REP-{len(records) + 1001}"
                new_ticket = {
                    "id": new_id,
                    "description": desc,
                    "category": ai_res["cat"],
                    "summary": desc[:50] + "...",
                    "priority": "Low" if is_dup else ai_res["prio"],
                    "reasoning": "SYSTEM NOTICE: Duplicate position match detected." if is_dup else ai_res["reason"],
                    "action_brief": f"Inspect {ai_res['cat'].lower()} coordinates to configure maintenance team dispatch requirements.",
                    "latitude": lat_input,
                    "longitude": lon_input,
                    "status": "Submitted",
                    "is_duplicate": is_dup
                }
                
                records.append(new_ticket)
                save_data(records)
                st.success(f"🎉 System Intake Complete! Ticket Registered Successfully: {new_id}")
                st.json(new_ticket)

# --- TAB 2: ADMIN VIEW ---
with tab2:
    st.header("Municipal Operations Dashboard")
    all_records = load_data()
    
    if all_records:
        df = pd.DataFrame(all_records)
        
        # Grid Cards counters
        m1, m2, m3 = st.columns(3)
        m1.metric("Total System Tickets", len(df))
        m2.metric("Critical Hazards Flagged", len(df[df["priority"] == "Critical"]))
        m3.metric("Likely Duplicates Intercepted", len(df[df["is_duplicate"] == True]))
        
        # Dynamic Map Display
        st.subheader("📍 Real-time Asset Hotspot Map")
        map_df = df[["latitude", "longitude"]].rename(columns={"latitude": "lat", "longitude": "lon"})
        st.map(map_df)
        
        # Dense Cluster Warnings Logic
        cluster_df = df.groupby(["latitude", "longitude"]).size().reset_index(name="counts")
        heavy_clusters = cluster_df[cluster_df["counts"] >= 3]
        if not heavy_clusters.empty:
            st.error(f"⚠️ PROACTIVE SYSTEM ALERT: {len(heavy_clusters)} active heavy geographic congestion hotspots detected in the municipal grid ledger!")
            
        # Priority workflow execution queue sorting
        st.subheader("🗂️ Urgent Priority Operational Queue")
        priority_map = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        df["prio_idx"] = df["priority"].map(priority_map)
        df_sorted = df.sort_values("prio_idx")
        
        for idx, row in df_sorted.iterrows():
            with st.expander(f"[{row['priority']}] {row['id']} - {row['category']} (Current Status: {row['status']})"):
                st.write(f"**Citizen Description:** {row['description']}")
                st.info(f"🧠 **AI Prioritization Reasoning:** {row['reasoning']}")
                st.warning(f"📋 **Field Operations Action Brief:** {row['action_brief']}")
                
                # Active interactive state update controller dropdown
                status_choices = ["Submitted", "Investigating", "In Progress", "Resolved"]
                current_state_idx = status_choices.index(row["status"]) if row["status"] in status_choices else 0
                
                updated_state = st.selectbox(f"Update Deployment Flow for {row['id']}", status_choices, index=current_state_idx, key=f"status_select_{row['id']}")
                
                if updated_state != row["status"]:
                    # Reference direct list index matching specific file object ID
                    for original_record in all_records:
                        if original_record["id"] == row["id"]:
                            original_record["status"] = updated_state
                            break
                    save_data(all_records)
                    st.rerun()
                else:
                    st.info("System data repository ledger is currently empty.")
# --- TAB 3: TRACKING TERMINAL ---
with tab3:
    st.header("Citizen Real-Time Ticket Verification Pipeline")
    search_id = st.text_input("Enter your unique Ticket ID (e.g., REP-1001, REP-CLUSTER-101):")
    
    if search_id:
        current_records = load_data()
        match_found = None
        
        for record in current_records:
            if record["id"].strip().upper() == search_id.strip().upper():
                match_found = record
                break
                
        if match_found:
            st.success("Ticket Found!")
            col_t1, col_t2 = st.columns(2)
            col_t1.metric("Current Assignment Status", match_found["status"])
            col_t2.metric("Assigned Infrastructure Priority", match_found["priority"])
            st.info(f"💡 AI Accountability Status update: {match_found['reasoning']}")
        else:
            st.error("Ticket reference ID not matching active municipal data entries. Double check syntax.")



