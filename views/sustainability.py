import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.translations import _
from utils.role_helper import is_action_allowed
from data.data_generator import generate_supply_chain_data

def show():
    st.title(f"🌱 {_('Sustainability & Green Logistics')}")
    st.markdown(_("**Track, analyze, and optimize your supply chain carbon footprint.**"))
    
    # Check permissions for actions
    # Assuming if user cannot edit, they cannot apply green alternatives.
    # We will use 'Admin' check for editing company-wide modes.
    can_edit = (st.session_state.get('user_role', 'Viewer') == 'Admin')
    can_simulate = is_action_allowed('simulate')
    
    # Initialize or get route modal split from session state
    if 'green_logistics_modes' not in st.session_state:
        # Default modal split [Sea, Air, Road]
        st.session_state['green_logistics_modes'] = {
            "Chennai - Singapore": "Air",
            "Thoothukudi - Europe": "Sea",
            "Coimbatore - Chennai": "Road",
            "Tiruppur - US": "Air"
        }
        
    modes = st.session_state['green_logistics_modes']
        
    # Standard CO2 impact multipliers (kg CO2 per ₹ of freight value)
    co2_multipliers = {
        "Sea": 0.05,
        "Air": 0.50,
        "Road": 0.15
    }
    
    # Mock freight values per container
    freight_value_per_container = 500000 # ₹5 Lakhs
    containers_per_month_per_route = 10
    
    route_details = []
    total_co2 = 0
    total_cost = 0
    
    for route, mode in modes.items():
        val = freight_value_per_container * containers_per_month_per_route
        co2 = val * co2_multipliers.get(mode, 0.1)
        route_details.append({
            "Route": route,
            "Current Mode": mode,
            "Freight Value (₹)": val,
            "CO₂ Emissions (kg)": co2
        })
        total_co2 += co2
        total_cost += val
        
    route_df = pd.DataFrame(route_details)
    
    # KPI metrics overlay
    st.markdown("""
    <style>
    .metrics-container {
        background: linear-gradient(135deg, #1e3a5f 0%, #294c63 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #44ff44;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric(_("Total Monthly Carbon Footprint"), f"{total_co2:,.0f} kg CO₂")
    col2.metric(_("Total Monthly Freight Cost"), f"₹{total_cost/100000:,.1f} Lakhs")
    col3.metric(_("Active Sustainable Routes"), sum([1 for m in modes.values() if m == "Sea"]))
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Charts and Tables
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f"### {_('CO₂ Contribution by Mode')}")
        # Aggregate by mode
        mode_co2 = route_df.groupby("Current Mode")["CO₂ Emissions (kg)"].sum().reset_index()
        mode_co2["Current Mode"] = mode_co2["Current Mode"].apply(lambda x: _(x))
        mode_co2 = mode_co2.rename(columns={
            "Current Mode": _("Current Mode"),
            "CO₂ Emissions (kg)": _("CO₂ Emissions (kg)")
        })
        
        fig_pie = px.pie(
            mode_co2, values=_('CO₂ Emissions (kg)'), names=_('Current Mode'), 
            hole=0.4,
            color=_('Current Mode'), 
            color_discrete_map={_('Sea'):'#44ff44', _('Air'):'#ff4444', _('Road'):'#ffaa00'}
        )
        fig_pie.update_layout(
            paper_bgcolor='#0e1117', 
            plot_bgcolor='#1a1a2e', 
            font=dict(color='white'),
            margin=dict(t=30, b=0, l=0, r=0)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.markdown(f"### {_('Green Alternatives')}")
        st.markdown(f"{_('Identify opportunities to reduce carbon footprint')}:")
        
        # Suggest alternatives mapping
        alternatives = {
            "Air": "Sea",
            "Road": "Sea"
        }
        
        opportunities_found = False
        for idx, row in route_df.iterrows():
            current_mode = row["Current Mode"]
            if current_mode in alternatives:
                opportunities_found = True
                alt_mode = alternatives[current_mode]
                alt_multiplier = co2_multipliers.get(alt_mode, 0.05) 
                
                alt_co2 = row["Freight Value (₹)"] * alt_multiplier
                savings_co2 = row["CO₂ Emissions (kg)"] - alt_co2
                
                # Mock cost impact: Sea is cheaper than Air, Sea cheaper than Road
                cost_impact = -(row["Freight Value (₹)"] * (0.6 if current_mode == "Air" else 0.2)) 
                
                with st.expander(f"♻️ {_('Switch')} **{row['Route']}** {_('from')} {_(current_mode)} {_('to')} {_(alt_mode)}"):
                    st.markdown(f"<span style='color: #44ff44;'>**Potential CO₂ Reduction:** -{savings_co2:,.0f} kg</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: #44ff44;'>**Est. Cost Impact:** ₹{cost_impact:,.0f} (Savings)</span>", unsafe_allow_html=True)
                    
                    if st.button(f"{_('Apply')} {_(alt_mode)} {_('to')} {row['Route']}", key=f"btn_{row['Route']}", disabled=not can_edit):
                        st.session_state['green_logistics_modes'][row['Route']] = alt_mode
                        st.toast(f"Applied {alt_mode} to {row['Route']}! 🌱")
                        st.rerun()
                        
        if not opportunities_found:
            st.success("All your primary routes are currently optimized for Sustainability! 🌍")
                        
    # Toggle for trade-off chart
    st.markdown("---")
    show_tradeoff = st.toggle("Show Cost-Resilience vs Green Trade-off", disabled=not can_simulate)
    
    if show_tradeoff:
        st.markdown("### ⚖️ Cost vs Resilience vs Emissions")
        
        # Mock scatter data
        scatter_data = pd.DataFrame({
            "Scenario": ["Current State", "Max Green", "Balanced", "Fastest Shipping"],
            "Cost (₹ Lakhs)": [total_cost/100000, (total_cost*0.6)/100000, (total_cost*0.8)/100000, (total_cost*1.5)/100000],
            "Resilience Score": [75, 60, 85, 90],
            "CO2 Emissions": [total_co2, total_co2 * 0.3, total_co2 * 0.5, total_co2 * 1.5]
        })
        
        # Rename columns to translated versions for the chart
        display_scatter = scatter_data.rename(columns={
            "Cost (₹ Lakhs)": _("Cost (₹ Lakhs)"),
            "Resilience Score": _("Resilience (%)"),
            "CO2 Emissions": _("CO₂ (kg)")
        })
        
        fig_scatter = px.scatter(
            display_scatter, 
            x=_("Cost (₹ Lakhs)"), 
            y=_("Resilience (%)"), 
            size=_("CO₂ (kg)"), 
            color="Scenario",
            color_discrete_sequence=['#ffaa00', '#44ff44', '#00d4ff', '#ff4444'],
            hover_name="Scenario", 
            size_max=40,
            text="Scenario"
        )
        
        fig_scatter.update_traces(textposition='top center')
        fig_scatter.update_layout(
            paper_bgcolor='#0e1117', 
            plot_bgcolor='#1a1a2e', 
            font=dict(color='white'),
            xaxis_title=f"{_('Cost (₹ Lakhs)')} (Lower is better)",
            yaxis_title=f"{_('Resilience (%)')} (Higher is better)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
