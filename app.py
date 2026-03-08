import streamlit as st
import sys
from pathlib import Path

# Page configuration
st.set_page_config(page_title="Supply Chain Control Tower", layout="wide", initial_sidebar_state="expanded")

# Import pages
from pages import landing, risk_dashboard, dna_visualizer, cascade_simulator, whatif_optimizer, case_studies

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stApp {background-color: #0e1117;}
    h1, h2, h3 {color: #00d4ff;}
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a7b 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🌐 Supply Chain Control Tower")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📊 Live Risk Dashboard", "🧬 DNA Visualizer", 
     "⚡ Cascade Simulator", "🎯 What-If Optimizer", "📚 Tamil Nadu Case Studies"]
)

# Route to pages
if page == "🏠 Home":
    landing.show()
elif page == "📊 Live Risk Dashboard":
    risk_dashboard.show()
elif page == "🧬 DNA Visualizer":
    dna_visualizer.show()
elif page == "⚡ Cascade Simulator":
    cascade_simulator.show()
elif page == "🎯 What-If Optimizer":
    whatif_optimizer.show()
elif page == "📚 Tamil Nadu Case Studies":
    case_studies.show()
