import json
import os
from data import auth_db

# Create a master test user
auth_db.create_user("hackathon_judge", "password123", "judge@demo.com")

# Mock company data
company_data = {
    "profile": {
        "name": "Demo Corp",
        "total_stock_value_lakhs": 500,
        "core_products": ["Automotive Parts"],
        "key_markets": ["Domestic (India)", "Europe"],
        "avg_revenue_lakhs": 2500,
        "investment_strategy": "Balanced"
    },
    "suppliers": [
        {
            "Supplier Name": "Chennai Auto Components",
            "Location (City, State)": "Chennai, Tamil Nadu",
            "Supplier Tier": "Tier 1 (Direct)",
            "Products Supplied": "Engine Parts",
            "Sourcing Type": "Single Source",
            "Historical Reliability (%)": 92,
            "Lead Time (Days)": 14,
            "Criticality": "High"
        }
    ],
    "inventory": [
         {
            "Warehouse Location": "Sriperumbudur Hub",
            "Products Stored": "Engine Parts",
            "Current Inventory Level": 5000,
            "Safety Stock Level": 1000,
            "Reorder Point": 1500,
            "Storage Capacity": 10000,
            "Is Perishable": False,
            "Shelf Life (Days)": 365
        }
    ],
    "logistics": {
        "primary_ports": ["Chennai Port"],
        "alternate_ports": ["Thoothukudi Port"],
        "primary_routes": "Chennai -> Europe",
        "partners": "Maersk Line",
        "transit_times": "21 Days",
        "modal_split": {"sea": 80, "air": 5, "road": 15},
        "avg_freight_cost": 50000
    },
    "risk_insights": {
        "top_customers": ["Volkswagen DE", "Tata Motors"],
        "customer_locations": "Germany, India",
        "late_penalty": "2% per day",
        "seasonal_peaks": ["Diwali"],
        "past_disruptions": ["Floods"],
        "risk_tolerance": "Medium - Balanced",
        "current_mitigations": ["Safety Stock"]
    }
}

auth_db.save_company_data("hackathon_judge", company_data)
print("Created 'hackathon_judge' test account with simulated company data.")
