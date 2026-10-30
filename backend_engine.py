import json
import os
import random
from openai import OpenAI

DB_FILE = "data.json"

# Fallback / Direct setup for OpenAI
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_HERE" else None

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

def run_ai_understanding_pipeline(description):
    """Parses text using Live LLM prompts, falling back safely to keywords on failure."""
    desc_lower = description.lower()
    
    if client:
        try:
            system_prompt = (
                "You are an expert civic management AI. Analyze the citizen complaint and return ONLY a "
                "JSON object with these exact keys: 'category', 'priority', 'summary', 'reasoning', 'action_brief'.\n"
                "Categories: [Waterlogging, Road Damage, Waste Management, Streetlights, Public Utility]\n"
                "Priorities: [Low, Medium, High, Critical]"
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": description}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices.message.content.strip())
        except Exception:
            pass
            
    # Rule-Based Local Fallback
    if "flood" in desc_lower or "water" in desc_lower or "rain" in desc_lower:
        return {
            "category": "Waterlogging", "priority": "High",
            "summary": "Water drainage pooling hazard reported near localized vectors.",
            "reasoning": "High priority assigned due to public transit impedance and vector health hazards.",
            "action_brief": "OPERATIONAL BRIEF: Deploy suction pumps to extract standing water."
        }
    elif "pothole" in desc_lower or "road" in desc_lower or "crack" in desc_lower:
        return {
            "category": "Road Damage", "priority": "Critical",
            "summary": "Structural degradation of asphalt transit lanes.",
            "reasoning": "Critical priority chosen to prevent immediate vehicle rim damage and swerve accidents.",
            "action_brief": "OPERATIONAL BRIEF: Dispatch asphalt patch vehicle for cold-mix cavity filling."
        }
    else:
        return {
            "category": "Public Utility", "priority": "Low",
            "summary": "Routine infrastructural utility report.",
            "reasoning": "Low priority given as the reported condition presents no immediate safety risks.",
            "action_brief": "OPERATIONAL BRIEF: Queue for routine maintenance assessment rotation."
        }

def seed_database_if_empty():
    current_data = load_data()
    if len(current_data) >= 40:
        return
        
    categories = ["Waterlogging", "Road Damage", "Waste Management", "Streetlights", "Public Utility"]
    center_lat, center_lon = 12.9716, 77.5946 
    synthetic_records = []
    
    for i in range(1, 31):
        cat = random.choice(categories)
        synthetic_records.append({
            "id": f"REP-{1000 + i}",
            "description": f"Standard public report regarding localized {cat.lower()} issues.",
            "category": cat,
            "summary": f"Routine tracking for {cat.lower()}.",
            "priority": random.choice(["Low", "Medium", "High", "Critical"]),
            "reasoning": "Automated ledger framework index mapping.",
            "action_brief": "Dispatch field crew to inspect assets.",
            "latitude": round(center_lat + random.uniform(-0.01, 0.01), 4),
            "longitude": round(center_lon + random.uniform(-0.01, 0.01), 4),
            "status": random.choice(["Submitted", "Investigating", "In Progress"]),
            "is_duplicate": False,
            "duplicate_of": None
        })
        
    for j in range(1, 7):
        synthetic_records.append({
            "id": f"REP-CLUSTER-{100 + j}",
            "description": "Compounded infrastructure system strain near central transit hub intersection node.",
            "category": random.choice(categories),
            "summary": "Compounded municipal load warning.",
            "priority": "Critical" if j % 2 == 0 else "High",
            "reasoning": "High risk designated due to dense cascading compound risks at transit nexus.",
            "action_brief": "URGENT RESILIENCE DISPATCH: Send multi-disciplinary crew immediately.",
            "latitude": 12.9750,
            "longitude": 77.5950,
            "status": "Submitted",
            "is_duplicate": False,
            "duplicate_of": None
        })
    save_data(synthetic_records)
    