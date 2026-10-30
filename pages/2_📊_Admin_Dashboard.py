import streamlit as st
import pandas as pd
import sys
import os
import streamlit as st
import pandas as pd
import backend_engine as backend


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import backend_engine as backend

st.markdown("""
    <style>
    .stApp { background-color: #0B0F19 !important; }
    
    /* Stylized Expandable Operational Grid Rows */
    .stHeader {
        background: #161B2A !important;
        border-radius: 10px !important;
    }
    
    /* Interactive Highlight Banners */
    div[data-testid="stExpander"] {
        background: rgba(22, 27, 42, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Stage 3 & 4: Operational Command Deck")
all_records = backend.load_data()

if all_records:
    df = pd.DataFrame(all_records)
    
    # Premium Metrics Interface Layout
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Ledger Entries", len(df))
    m2.metric("Critical Safety Liabilities", len(df[df["priority"] == "Critical"]))
    m3.metric("Spam Duplicates Intercepted", len(df[df["is_duplicate"] == True]))
    
    st.write("---")
    st.subheader("📍 Real-time Asset Hotspot Mapping Profile")
    map_df = df[["latitude", "longitude"]].rename(columns={"latitude": "lat", "longitude": "lon"})
    st.map(map_df)
    
    # Pandas Geo Clustering Alert Engine
    cluster_df = df.groupby(["latitude", "longitude"]).size().reset_index(name="counts")
    heavy_clusters = cluster_df[cluster_df["counts"] >= 3]
    if not heavy_clusters.empty:
        st.error(f"🚨 CASCADING STRUCTURAL HAZARD: {len(heavy_clusters)} active heavy infrastructure congestion zones identified in local sectors!")
        
    st.write("---")
    st.subheader("🗂️ Urgent Deployment Workflow Queue")
    priority_map = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    df["prio_idx"] = df["priority"].map(priority_map)
    df_sorted = df.sort_values("prio_idx")
    
    for idx, row in df_sorted.iterrows():
        badge = "🛑 DUPLICATE PROFILE" if row['is_duplicate'] else "💎 ORIGINAL RECORD"
        with st.expander(f"[{row['priority']}] {row['id']} - {row['category']} ({badge} | State: {row['status']})"):
            st.write(f"**Raw Context Description:** {row['description']}")
            st.info(f"🧠 **AI Prioritisation Analysis:** {row['reasoning']}")
            st.warning(f"📋 **Field Crew Action Directive:** {row['action_brief']}")
            
            status_choices = ["Submitted", "Investigating", "In Progress", "Resolved"]
            current_state_idx = status_choices.index(row["status"]) if row["status"] in status_choices else 0
            
            updated_state = st.selectbox(f"Modify Operational Phase for {row['id']}", status_choices, index=current_state_idx, key=f"select_{row['id']}")
            
            if updated_state != row["status"]:
                for original_record in all_records:
                    if original_record["id"] == row["id"]:
                        original_record["status"] = updated_state
                        break
                backend.save_data(all_records)
                st.rerun()
else:
    st.info("System storage array ledger is empty.")
