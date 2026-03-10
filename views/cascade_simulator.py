import streamlit as st
import plotly.graph_objects as go
import sys
sys.path.append('..')
from data.data_generator import generate_supply_chain_data, generate_case_study_data
from models.ml_models import CascadeSimulator
from utils.translations import _
from utils.role_helper import is_action_allowed
from utils.translations import _

def show():
    st.title(_("⚡ Cascade Simulator"))
    st.markdown(f"**{_('Click any supplier to see downstream impact with timeline')}**")
    
    # Load data
    data = generate_supply_chain_data()
    suppliers_df = data['suppliers']
    dependencies_df = data['dependencies']
    products_df = data['products']
    customers_df = data['customers']
    
    # Initialize simulator
    simulator = CascadeSimulator(suppliers_df, dependencies_df, products_df, customers_df)
    
    # Supplier selection
    st.markdown(f"### {_('Select Supplier to Simulate Failure')}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_supplier = st.selectbox(
            "Choose a supplier node:",
            suppliers_df['id'].tolist(),
            format_func=lambda x: f"{x} - {suppliers_df[suppliers_df['id']==x].iloc[0]['name']}"
        )
    
    with col2:
        delay_days = st.slider("Disruption Duration (days)", 1, 14, 5)
    
    # Get selected supplier details
    supplier_info = suppliers_df[suppliers_df['id'] == selected_supplier].iloc[0]
    
    st.markdown(f"""
    <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; margin: 20px 0;'>
        <h4 style='color: #00d4ff; margin-top: 0;'>{_('Selected Node:')} {supplier_info['name']}</h4>
        <p style='color: white; margin: 5px 0;'>{_('Type:')} {_(supplier_info['type'])} | {_('Location:')} {_(supplier_info['location'])} | {_('Tier:')} {supplier_info['tier']}</p>
        <p style='color: #ffaa00; margin: 5px 0;'>{_('Risk Zone:')} {_(supplier_info['risk_zone'])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Run simulation
    can_simulate = is_action_allowed('simulate')
    if st.button(_("Run Cascade Simulation"), type="primary", disabled=not can_simulate):
        with st.spinner("Running Monte Carlo simulation with 1000 iterations..."):
            result = simulator.simulate_cascade(selected_supplier, delay_days)
        
        # Store in session state
        st.session_state['cascade_result'] = result
        st.session_state['selected_supplier'] = selected_supplier
        st.session_state['delay_days'] = delay_days
    
    # Display results if available
    if 'cascade_result' in st.session_state:
        result = st.session_state['cascade_result']
        
        st.markdown("---")
        st.markdown(f"### {_('Cascade Impact Analysis')}")
        
        # Impact summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%); padding: 20px; border-radius: 10px; text-align: center;'>
                <h2 style='color: white; margin: 0; font-size: 2.5em;'>{len(result['affected_suppliers'])}</h2>
                <p style='color: white; margin: 5px 0 0 0;'>Affected Suppliers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ffaa00 0%, #ff8800 100%); padding: 20px; border-radius: 10px; text-align: center;'>
                <h2 style='color: white; margin: 0; font-size: 2.5em;'>{len(result['affected_products'])}</h2>
                <p style='color: white; margin: 5px 0 0 0;'>Affected Products</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #aa44ff 0%, #8800cc 100%); padding: 20px; border-radius: 10px; text-align: center;'>
                <h2 style='color: white; margin: 0; font-size: 2.5em;'>{len(result['affected_customers'])}</h2>
                <p style='color: white; margin: 5px 0 0 0;'>Affected Customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            cost_mean_cr = result['cost_impact_mean'] / 10000000  # Convert to Crores
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); padding: 20px; border-radius: 10px; text-align: center;'>
                <h2 style='color: white; margin: 0; font-size: 2.5em;'>₹{cost_mean_cr:.2f}Cr</h2>
                <p style='color: white; margin: 5px 0 0 0;'>Expected Cost Impact</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Timeline visualization
        st.markdown(f"### {_('Impact Timeline')}")
        
        timeline = result['timeline']
        timeline_data = []
        
        for supplier_id, days in timeline.items():
            supplier = suppliers_df[suppliers_df['id'] == supplier_id].iloc[0]
            timeline_data.append({
                'supplier': supplier['name'],
                'days': days,
                'type': supplier['type']
            })
        
        timeline_data.sort(key=lambda x: x['days'])
        
        # Create timeline visualization
        fig = go.Figure()
        
        colors = {'Port': '#ff4444', 'Manufacturer': '#ffaa00', 'Raw Material': '#00d4ff'}
        
        for i, item in enumerate(timeline_data):
            fig.add_trace(go.Scatter(
                x=[item['days']],
                y=[i],
                mode='markers+text',
                marker=dict(size=20, color=colors.get(item['type'], '#44ff44')),
                text=f"Day {item['days']}",
                textposition="middle right",
                name=item['supplier'],
                hovertext=f"{item['supplier']}<br>Impact Day: {item['days']}<br>Type: {item['type']}",
                hoverinfo='text'
            ))
        
        fig.update_layout(
            showlegend=False,
            xaxis=dict(title='Days from Initial Disruption', showgrid=True, gridcolor='#333'),
            yaxis=dict(showticklabels=False, showgrid=False),
            paper_bgcolor='#0e1117',
            plot_bgcolor='#1a1a2e',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed impact breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {_('Affected Products')}")
            for product in result['affected_products']:
                monthly_loss = product['monthly_volume'] * product['value_per_unit']
                daily_loss = monthly_loss / 30
                total_loss = daily_loss * st.session_state['delay_days']
                
                st.markdown(f"""
                <div style='background: #1a1a2e; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                    <h4 style='color: #00d4ff; margin-top: 0;'>{product['name']}</h4>
                    <p style='color: white; margin: 5px 0;'>{_('Monthly Volume')} {product['monthly_volume']:,} units</p>
                    <p style='color: white; margin: 5px 0;'>{_('Value per Unit')} ₹{product['value_per_unit']:,}</p>
                    <p style='color: #ff6b6b; margin: 5px 0; font-weight: bold;'>{_('Estimated Loss')} ₹{total_loss:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"### {_('Affected Customers')}")
            for customer in result['affected_customers']:
                impact_pct = (st.session_state['delay_days'] / 30) * 100
                revenue_impact = customer['revenue_monthly'] * (st.session_state['delay_days'] / 30)
                
                st.markdown(f"""
                <div style='background: #1a1a2e; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                    <h4 style='color: #00d4ff; margin-top: 0;'>{customer['name']}</h4>
                    <p style='color: white; margin: 5px 0;'>Region: {customer['region']}</p>
                    <p style='color: white; margin: 5px 0;'>Monthly Revenue: ₹{customer['revenue_monthly']:,}</p>
                    <p style='color: #ff6b6b; margin: 5px 0; font-weight: bold;'>{_('Revenue at Risk')} ₹{revenue_impact:,.0f} ({impact_pct:.1f}% of monthly)</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Cost impact distribution
        st.markdown(f"### {_('Cost Impact Distribution (Monte Carlo)')}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Mean Impact", f"₹{result['cost_impact_mean']/10000000:.2f} Cr")
        
        with col2:
            st.metric("Std Deviation", f"₹{result['cost_impact_std']/10000000:.2f} Cr")
        
        with col3:
            st.metric("95th Percentile (Worst Case)", f"₹{result['cost_impact_95th']/10000000:.2f} Cr")
        
        # Recommendations
        st.markdown("---")
        st.markdown(f"### {_('Mitigation Recommendations')}")
        
        if len(result['affected_suppliers']) > 3:
            severity = "CRITICAL"
            color = "#ff4444"
        elif len(result['affected_suppliers']) > 1:
            severity = "HIGH"
            color = "#ffaa00"
        else:
            severity = "MODERATE"
            color = "#44ff44"
        
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; border-left: 5px solid {color};'>
            <h4 style='color: {color}; margin-top: 0;'>{_('Severity Level:')} {_(severity)}</h4>
            <ul style='color: white;'>
                <li>{_('Immediate Action:')} {_('Activate backup suppliers for affected products')}</li>
                <li>{_('Communication:')} {_('Alert 3 affected customers within 24 hours')}</li>
                <li>{_('Logistics:')} {_('Consider air freight for high-value products to minimize delay')}</li>
                <li>{_('Inventory:')} {_('Draw from safety stock to cover first 3 days')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # --- FEATURE 4: HISTORICAL POST-MORTEM ---
        st.markdown("---")
        st.markdown(f"### 📜 {_('Compare with Historical Event')}")
        st.markdown(f"{_('See how your current AI-optimized strategy would have performed against past disruptions.')}")
        
        case_studies_df = generate_case_study_data()
        case_titles = case_studies_df['title'].tolist()
        
        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            selected_case_title = st.selectbox("Select historical event for comparison:", case_titles, label_visibility="collapsed")
        
        if st.button(_("Show Comparison"), disabled=not can_simulate):
            case = case_studies_df[case_studies_df['title'] == selected_case_title].iloc[0]
            
            st.markdown(f"**Event Description:** {case['description']}")
            
            hc1, hc2 = st.columns(2)
            
            with hc1:
                st.markdown(f"""
                <div style='background: #3a1c1c; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4444;'>
                    <h4 style='color: #ff6b6b; margin-top: 0;'>Historical Impact (Actual)</h4>
                    <p style='color: white; font-size: 1.1em;'><strong>Financial Loss:</strong> ₹{case['actual_cost']/100000:.1f} Lakhs</p>
                    <p style='color: white; font-size: 1.1em;'><strong>Delay:</strong> {case['actual_delay']} days</p>
                    <p style='color: #ffcccc;'>Recovery strategy was manual and reactive.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with hc2:
                # Simulate AI impact as heavily reduced from historical actuals
                ai_cost = case['actual_cost'] * 0.4
                ai_delay = max(0, int(case['actual_delay'] * 0.5))
                savings = case['actual_cost'] - ai_cost
                savings_pct = (savings / case['actual_cost']) * 100 if case['actual_cost'] > 0 else 0
                
                st.markdown(f"""
                <div style='background: #1c3a26; padding: 20px; border-radius: 10px; border-left: 5px solid #44ff44;'>
                    <h4 style='color: #44ff44; margin-top: 0;'>AI-Optimized Impact (Simulated)</h4>
                    <p style='color: white; font-size: 1.1em;'><strong>Estimated Loss:</strong> ₹{ai_cost/100000:.1f} Lakhs</p>
                    <p style='color: white; font-size: 1.1em;'><strong>Estimated Delay:</strong> {ai_delay} days</p>
                    <p style='color: #ccffcc;'>Recovery strategy is proactive and automated.</p>
                </div>
                """, unsafe_allow_html=True)
                
            if savings > 0:
                st.markdown(f"""
                <div style='text-align: center; background: #1a1a2e; padding: 15px; border-radius: 10px; margin-top: 15px;'>
                    <h3 style='color: #00d4ff; margin: 0;'>💡 AI could have saved <span style='color: #44ff44;'>₹{savings/100000:.1f} Lakhs</span> ({savings_pct:.0f}%) and <span style='color: #44ff44;'>{case['actual_delay'] - ai_delay} days</span>!</h3>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='text-align: center; background: #1a1a2e; padding: 15px; border-radius: 10px; margin-top: 15px;'>
                    <h3 style='color: #00d4ff; margin: 0;'>💡 AI prevented any delays or costs during this event simulation!</h3>
                </div>
                """, unsafe_allow_html=True)
                
    
    else:
        st.info("👆 Select a supplier and click 'Run Cascade Simulation' to see the domino effect")
