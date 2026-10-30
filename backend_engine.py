import json
import os
import random
import math

DB_FILE = "data.json"

# HACKATHON API CONFIG
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"
client = None # Setup: Replace with OpenAI(api_key=OPENAI_API_KEY) if using live keys

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

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates exact metric distance to catch smart proximity duplicates."""
    radius_earth = 6371000  # Meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (math.sin(delta_phi / 2) ** 2 + 
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    return radius_earth * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def run_ai_understanding_pipeline(description):
    """Transforms raw complaints into highly analytical structured tokens."""
    desc_lower = description.lower()
    
    # Rule-Based Fail-Safe Core Processing Engine
    if "flood" in desc_lower or "water" in desc_lower or "rain" in desc_lower or "drain" in desc_lower:
        return {
            "category": "Waterlogging", "priority": "High",
            "summary": "Water drainage pooling hazard reported near localized corridors.",
            "reasoning": "High priority assigned due to immediate pedestrian impedance and vector-borne public health hazards.",
            "action_brief": "OPERATIONAL BRIEF: Deploy emergency suction pumps to extract standing water and clear drain screens."
        }
    elif "pothole" in desc_lower or "road" in desc_lower or "crack" in desc_lower or "asphalt" in desc_lower:
        return {
            "category": "Road Damage", "priority": "Critical",
            "summary": "Structural degradation of active municipal transit lanes.",
            "reasoning": "Critical priority chosen to eliminate immediate vehicle tire destruction and high-speed swerving crashes.",
            "action_brief": "OPERATIONAL BRIEF: Dispatch asphalt repair vehicle for immediate cold-mix structural cavity patching."
        }
    elif "dark" in desc_lower or "light" in desc_lower or "lamp" in desc_lower or "bulb" in desc_lower:
        return {
            "category": "Streetlights", "priority": "Medium",
            "summary": "Illumination matrix circuit failure.",
            "reasoning": "Medium priority assigned due to increased pedestrian safety vulnerabilities during low-light cycles.",
            "action_brief": "OPERATIONAL BRIEF: Send utility electrician to inspect pole junction arrays and swap blown lamps."
        }
    else:
        return {
            "category": "Public Utility", "priority": "Low",
            "summary": "Routine infrastructural asset condition report.",
            "reasoning": "Low priority given as the reported liability lacks cascading public safety or arterial block risks.",
            "action_brief": "OPERATIONAL BRIEF: Log data into standard maintenance queue for localized rotation squads."
        }

def seed_database_if_empty():
    current_data = load_data()
    if len(current_data) >= 40:
        return
        
    categories = ["Waterlogging", "Road Damage", "Waste Management", "Streetlights", "Public Utility"]
    center_lat, center_lon = 12.9716, 77.5946 
    synthetic_records = []
    
    # Populate base dataset rows
    for i in range(1, 31):
        cat = random.choice(categories)
        synthetic_records.append({
            "id": f"REP-{1000 + i}",
            "description": f"Public citizen ticket reporting localized asset failure requiring engineering tracking.",
            "category": cat,
            "summary": f"Routine tracking for regional {cat.lower()}.",
            "priority": random.choice(["Low", "Medium", "High", "Critical"]),
            "reasoning": "Automated baseline lookup prioritizing parameters.",
            "action_brief": "Deploy field inspectors to gauge degradation parameters.",
            "latitude": round(center_lat + random.uniform(-0.01, 0.01), 4),
            "longitude": round(center_lon + random.uniform(-0.01, 0.01), 4),
            "status": random.choice(["Submitted", "Investigating", "In Progress"]),
            "is_duplicate": False,
            "duplicate_of": None
        })
        
    # Inject heavy geographic cluster (Overlapping points at same intersection)
    for j in range(1, 7):
        synthetic_records.append({
            "id": f"REP-CLUSTER-{100 + j}",
            "description": f"Cascading system failure causing compound structural damage near central transit junction node.",
            "category": random.choice(categories),
            "summary": "Compounded multi-layer infrastructure structural overload alert.",
            "priority": "Critical" if j % 2 == 0 else "High",
            "reasoning": "Priority escalated due to heavy risk of cascading utility destruction across intersecting lines.",
            "action_brief": "URGENT COMPREHENSIVE REPAIR: Deploy multi-disciplinary emergency squad for full system bypass.",
            "latitude": 12.9750,
            "longitude": 77.5950,
            "status": "Submitted",
            "is_duplicate": False,
            "duplicate_of": None
        })
    save_data(synthetic_records)
