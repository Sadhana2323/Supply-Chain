import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate realistic Tamil Nadu supply chain data
def generate_supply_chain_data():
    """Generate synthetic supply chain network data for Tamil Nadu"""
    
    # Suppliers with Tamil Nadu context
    suppliers = [
        {"id": "S001", "name": "Chennai Port Authority", "type": "Port", "location": "Chennai", "lat": 13.0827, "lon": 80.2707, "tier": 1, "risk_zone": "Flood-prone"},
        {"id": "S002", "name": "Thoothukudi VOC Port", "type": "Port", "location": "Thoothukudi", "lat": 8.7642, "lon": 78.1348, "tier": 1, "risk_zone": "Cyclone-prone"},
        {"id": "S003", "name": "Krishnapatnam Port", "type": "Port", "location": "Nellore", "lat": 14.2500, "lon": 80.0500, "tier": 1, "risk_zone": "Moderate"},
        {"id": "S004", "name": "Tiruppur Knitwear Exports Ltd", "type": "Manufacturer", "location": "Tiruppur", "lat": 11.1085, "lon": 77.3411, "tier": 2, "risk_zone": "Low"},
        {"id": "S005", "name": "Coimbatore Engineering Works", "type": "Manufacturer", "location": "Coimbatore", "lat": 11.0168, "lon": 76.9558, "tier": 2, "risk_zone": "Low"},
        {"id": "S006", "name": "Karur Home Textiles Co", "type": "Manufacturer", "location": "Karur", "lat": 10.9601, "lon": 78.0766, "tier": 2, "risk_zone": "Moderate"},
        {"id": "S007", "name": "Chennai Cotton Suppliers", "type": "Raw Material", "location": "Chennai", "lat": 13.0500, "lon": 80.2000, "tier": 3, "risk_zone": "Flood-prone"},
        {"id": "S008", "name": "Madurai Dye Works", "type": "Raw Material", "location": "Madurai", "lat": 9.9252, "lon": 78.1198, "tier": 3, "risk_zone": "Low"},
        {"id": "S009", "name": "Salem Steel Components", "type": "Raw Material", "location": "Salem", "lat": 11.6643, "lon": 78.1460, "tier": 3, "risk_zone": "Low"},
        {"id": "S010", "name": "Erode Yarn Suppliers", "type": "Raw Material", "location": "Erode", "lat": 11.3410, "lon": 77.7172, "tier": 3, "risk_zone": "Moderate"},
    ]
    
    # Dependencies (edges in supply chain network)
    dependencies = [
        {"from": "S007", "to": "S004", "product": "Cotton", "lead_time": 3, "single_source": True},
        {"from": "S008", "to": "S004", "product": "Dyes", "lead_time": 2, "single_source": True},
        {"from": "S009", "to": "S005", "product": "Steel", "lead_time": 5, "single_source": True},
        {"from": "S010", "to": "S006", "product": "Yarn", "lead_time": 4, "single_source": True},
        {"from": "S004", "to": "S001", "product": "Knitwear", "lead_time": 2, "single_source": False},
        {"from": "S005", "to": "S001", "product": "Machinery", "lead_time": 3, "single_source": False},
        {"from": "S005", "to": "S003", "product": "Machinery", "lead_time": 4, "single_source": False},
        {"from": "S006", "to": "S002", "product": "Textiles", "lead_time": 2, "single_source": True},
        {"from": "S004", "to": "S002", "product": "Knitwear", "lead_time": 3, "single_source": False},
    ]
    
    # Real-time risk events
    risk_events = [
        {"port": "Chennai Port", "type": "Weather", "severity": "High", "description": "Heavy rainfall warning - 150mm expected", "impact": "2-3 day delay", "probability": 0.75},
        {"port": "Thoothukudi VOC Port", "type": "Geopolitical", "severity": "Medium", "description": "Labor strike planned", "impact": "1-2 day delay", "probability": 0.60},
        {"port": "Krishnapatnam Port", "type": "Congestion", "severity": "Low", "description": "Moderate vessel queue", "impact": "4-6 hour delay", "probability": 0.30},
        {"port": "Chennai Port", "type": "Infrastructure", "severity": "Medium", "description": "Crane maintenance scheduled", "impact": "1 day delay", "probability": 0.50},
    ]
    
    # Products and customers
    products = [
        {"id": "P001", "name": "Cotton Knitwear", "supplier": "S004", "port": "S001", "monthly_volume": 50000, "value_per_unit": 15},
        {"id": "P002", "name": "Industrial Machinery", "supplier": "S005", "port": "S001", "monthly_volume": 200, "value_per_unit": 25000},
        {"id": "P003", "name": "Home Textiles", "supplier": "S006", "port": "S002", "monthly_volume": 30000, "value_per_unit": 20},
        {"id": "P004", "name": "Export Knitwear", "supplier": "S004", "port": "S002", "monthly_volume": 40000, "value_per_unit": 18},
    ]
    
    customers = [
        {"id": "C001", "name": "US Retail Chain", "region": "North America", "products": ["P001", "P004"], "revenue_monthly": 1200000},
        {"id": "C002", "name": "European Importers", "region": "Europe", "products": ["P002", "P003"], "revenue_monthly": 800000},
        {"id": "C003", "name": "Middle East Distributors", "region": "Middle East", "products": ["P001", "P003"], "revenue_monthly": 600000},
    ]
    
    return {
        "suppliers": pd.DataFrame(suppliers),
        "dependencies": pd.DataFrame(dependencies),
        "risk_events": pd.DataFrame(risk_events),
        "products": pd.DataFrame(products),
        "customers": pd.DataFrame(customers)
    }

def generate_historical_disruptions():
    """Generate historical disruption data for ML training"""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2025-01-01', freq='D')
    
    disruptions = []
    for date in dates:
        # Simulate disruptions with seasonal patterns
        month = date.month
        is_monsoon = month in [6, 7, 8, 9, 10, 11]  # Monsoon season
        
        base_prob = 0.15 if is_monsoon else 0.05
        
        if np.random.random() < base_prob:
            disruptions.append({
                'date': date,
                'location': np.random.choice(['Chennai', 'Thoothukudi', 'Coimbatore', 'Tiruppur']),
                'type': np.random.choice(['Weather', 'Infrastructure', 'Labor', 'Geopolitical']),
                'severity': np.random.choice(['Low', 'Medium', 'High'], p=[0.5, 0.3, 0.2]),
                'delay_days': np.random.randint(1, 8),
                'cost_impact': np.random.randint(10000, 500000)
            })
    
    return pd.DataFrame(disruptions)

def generate_case_study_data():
    """Generate Tamil Nadu specific case studies from 2023-2025"""
    case_studies = [
        {
            "id": "CS001",
            "title": "Chennai Floods - December 2023",
            "date": "2023-12-15",
            "description": "Heavy rainfall caused Chennai Port closure for 4 days, affecting 15 export shipments",
            "affected_suppliers": ["S001", "S007"],
            "affected_products": ["P001", "P004"],
            "actual_delay": 6,
            "actual_cost": 450000,
            "mitigation_used": "Rerouted through Krishnapatnam Port",
            "lessons": "Need alternate port strategy for monsoon season"
        },
        {
            "id": "CS002",
            "title": "Thoothukudi Port Closure - March 2024",
            "date": "2024-03-10",
            "description": "Environmental protests led to 3-day port closure affecting textile exports",
            "affected_suppliers": ["S002", "S006"],
            "affected_products": ["P003"],
            "actual_delay": 5,
            "actual_cost": 320000,
            "mitigation_used": "Air freight for urgent orders",
            "lessons": "Diversify export ports for critical products"
        },
        {
            "id": "CS003",
            "title": "US Tariff Shock - July 2024",
            "date": "2024-07-01",
            "description": "Sudden 25% tariff on textile imports caused demand spike for pre-tariff shipments",
            "affected_suppliers": ["S004", "S006"],
            "affected_products": ["P001", "P003", "P004"],
            "actual_delay": 0,
            "actual_cost": 0,
            "mitigation_used": "Increased production capacity by 40%",
            "lessons": "Need demand surge capacity planning"
        }
    ]
    
    return pd.DataFrame(case_studies)
