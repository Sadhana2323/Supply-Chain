"""
Quick test script to verify all modules load correctly
"""
import sys
print("Testing Supply Chain Control Tower modules...")

# Test data generator
print("\n1. Testing data generator...")
from data.data_generator import generate_supply_chain_data, generate_historical_disruptions, generate_case_study_data
data = generate_supply_chain_data()
print(f"   [OK] Generated {len(data['suppliers'])} suppliers")
print(f"   [OK] Generated {len(data['dependencies'])} dependencies")
print(f"   [OK] Generated {len(data['risk_events'])} risk events")

# Test ML models
print("\n2. Testing ML models...")
from models.ml_models import DisruptionPredictor, CascadeSimulator, WhatIfOptimizer
historical = generate_historical_disruptions()
predictor = DisruptionPredictor()
predictor.train(historical)
print(f"   [OK] Trained predictor on {len(historical)} historical events")

simulator = CascadeSimulator(data['suppliers'], data['dependencies'], data['products'], data['customers'])
print(f"   [OK] Initialized cascade simulator")

optimizer = WhatIfOptimizer(data['products'])
print(f"   [OK] Initialized what-if optimizer")

# Test pages import
print("\n3. Testing view modules...")
from views import landing, risk_dashboard, dna_visualizer, cascade_simulator, whatif_optimizer, case_studies
print("   [OK] All view modules loaded successfully")

print("\n[SUCCESS] All tests passed! Application is ready to run.")
print("\nTo start the application, run:")
print("   python -m streamlit run app.py")
