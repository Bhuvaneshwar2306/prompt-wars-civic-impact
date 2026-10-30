import streamlit as st
import pandas as pd
import backend_engine as backend

st.header("Stage 3 & 4: Operations Dashboard")
all_records = backend.load_data()

if all_records:
    df = pd.DataFrame(all_records)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total System Tickets", len(df))
    m2.metric("Critical Hazards Flagged", len(df[df["priority"] == "Critical"]))
    m3.metric("Likely Duplicates Intercepted", len(df[df["is_duplicate"] == True]))
    
    st.subheader("📍 Real-time Asset Hotspot Map")
    map_df = df[["latitude", "longitude"]].rename(columns={"latitude": "lat", "longitude": "lon"})
    st.map(map_df)
    
    cluster_df = df.groupby(["latitude", "longitude"]).size().reset_index(name="counts")
    heavy_clusters = cluster_df[cluster_df["counts"] >= 3]
    if not heavy_clusters.empty:
        st.error(f"⚠️ PROACTIVE ALERT: {len(heavy_clusters)} active heavy geographic congestion hotspots detected!")
        
    st.subheader("🗂️ Urgent Priority Operational Queue")
    priority_map = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    df["prio_idx"] = df["priority"].map(priority_map)
    df_sorted = df.sort_values("prio_idx")
    
    for idx, row in df_sorted.iterrows():
        badge = "🚨 DUP LINK" if row['is_duplicate'] else "📋 ORIGINAL"
        with st.expander(f"[{row['priority']}] {row['id']} - {row['category']} ({badge} | Status: {row['status']})"):
            st.write(f"**Citizen Description:** {row['description']}")
            st.info(f"🧠 **AI Reason:** {row['reasoning']}")
            st.warning(f"📋 **Action Brief:** {row['action_brief']}")
            
            status_choices = ["Submitted", "Investigating", "In Progress", "Resolved"]
            current_state_idx = status_choices.index(row["status"]) if row["status"] in status_choices else 0
            
            updated_state = st.selectbox(f"Update Deployment Flow for {row['id']}", status_choices, index=current_state_idx, key=f"status_select_{row['id']}")
            
            if updated_state != row["status"]:
                for original_record in all_records:
                    if original_record["id"] == row["id"]:
                        original_record["status"] = updated_state
                        break
                backend.save_data(all_records)
                st.author_rerun() if hasattr(st, "author_rerun") else st.rerun()
else:
    st.info("No active tickets available in storage.")
