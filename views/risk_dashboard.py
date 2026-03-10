import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
from data.data_generator import generate_supply_chain_data
from utils.translations import _

def show():
    st.title(_("📊 Live Risk Dashboard Page"))
    st.markdown(f"**{_('Real-time monitoring of supply chain risks across Tamil Nadu')}**")
    
    # Load data
    data = generate_supply_chain_data()
    suppliers_df = data['suppliers']
    risk_events = data['risk_events']
    
    company_profile = data.get('company_profile')
    if company_profile:
        st.info(f"🏢 **{_('Active Company Profile')}**: {company_profile.get('name', 'N/A')} | **{_('Avg Revenue')}**: ₹{company_profile.get('avg_revenue_lakhs', 0)}L")

    
    # Risk Summary Cards
    st.markdown(f"### {_('Current Risk Status')}")
    col1, col2, col3, col4 = st.columns(4)
    
    high_risks = len(risk_events[risk_events['severity'] == 'High'])
    medium_risks = len(risk_events[risk_events['severity'] == 'Medium'])
    low_risks = len(risk_events[risk_events['severity'] == 'Low'])
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%); padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: white; margin: 0; font-size: 2.5em;'>{high_risks}</h2>
            <p style='color: white; margin: 5px 0 0 0;'>{_('High Risk Alerts')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ffaa00 0%, #ff8800 100%); padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: white; margin: 0; font-size: 2.5em;'>{medium_risks}</h2>
            <p style='color: white; margin: 5px 0 0 0;'>{_('Medium Risk Alerts')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #44ff44 0%, #00cc00 100%); padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: white; margin: 0; font-size: 2.5em;'>{low_risks}</h2>
            <p style='color: white; margin: 5px 0 0 0;'>{_('Low Risk Alerts')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_prob = risk_events['probability'].mean() * 100
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: white; margin: 0; font-size: 2.5em;'>{avg_prob:.0f}%</h2>
            <p style='color: white; margin: 5px 0 0 0;'>{_('Avg Probability')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Map
    st.markdown(f"### {_('Geographic Risk Map - Tamil Nadu Ports & Suppliers')}")
    
    # Create map with risk levels
    fig = go.Figure()
    
    # Color mapping for risk zones
    risk_colors = {
        'Flood-prone': '#ff4444',
        'Cyclone-prone': '#ff8800',
        'Moderate': '#ffaa00',
        'Low': '#44ff44'
    }
    
    for idx, supplier in suppliers_df.iterrows():
        color = risk_colors.get(supplier['risk_zone'], '#00d4ff')
        size = 20 if supplier['tier'] == 1 else 15
        
        fig.add_trace(go.Scattergeo(
            lon=[supplier['lon']],
            lat=[supplier['lat']],
            text=f"<b>{supplier['name']}</b><br>Type: {supplier['type']}<br>Risk Zone: {supplier['risk_zone']}<br>Tier: {supplier['tier']}",
            mode='markers',
            marker=dict(size=size, color=color, line=dict(width=2, color='white')),
            name=supplier['risk_zone'],
            showlegend=True if suppliers_df[suppliers_df['risk_zone'] == supplier['risk_zone']].index[0] == supplier.name else False
        ))
    
    fig.update_geos(
        center=dict(lat=11.0, lon=78.5),
        projection_scale=8,
        visible=True,
        showcountries=True,
        countrycolor="darkgray"
    )
    
    fig.update_layout(
        height=500,
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='#0e1117',
        geo=dict(bgcolor='#1a1a2e'),
        showlegend=True,
        legend=dict(bgcolor='#1a1a2e', font=dict(color='white'))
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Live Risk Events Table
    st.markdown(f"### {_('Active Risk Events')}")
    
    for idx, event in risk_events.iterrows():
        severity_color = {'High': '#ff4444', 'Medium': '#ffaa00', 'Low': '#44ff44'}[event['severity']]
        severity_icon = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}[event['severity']]
        
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; margin: 10px 0; border-left: 5px solid {severity_color};'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <h4 style='color: {severity_color}; margin: 0;'>{severity_icon} {_(f"{event['port']} - {event['type']}")}</h4>
                    <p style='color: #a0a0a0; margin: 5px 0;'>{_(event['description'])}</p>
                    <p style='color: #00d4ff; margin: 5px 0;'><strong>{_('Expected Impact:')}</strong> {_(event['impact'])}</p>
                </div>
                <div style='text-align: right;'>
                    <h2 style='color: white; margin: 0;'>{event['probability']*100:.0f}%</h2>
                    <p style='color: #a0a0a0; margin: 0; font-size: 0.9em;'>{_('Probability:')}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Risk Trend Chart
    st.markdown(f"### {_('Risk Probability Trends')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk by type
        risk_by_type = risk_events.groupby('type')['probability'].mean().reset_index()
        fig_type = px.bar(
            risk_by_type,
            x='type',
            y='probability',
            title='Average Risk Probability by Type',
            color='probability',
            color_continuous_scale=['#44ff44', '#ffaa00', '#ff4444']
        )
        fig_type.update_layout(
            paper_bgcolor='#0e1117',
            plot_bgcolor='#1a1a2e',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#333')
        )
        st.plotly_chart(fig_type, use_container_width=True)
    
    with col2:
        # Risk by severity
        severity_counts = risk_events['severity'].value_counts().reset_index()
        severity_counts.columns = ['severity', 'count']
        fig_severity = px.pie(
            severity_counts,
            values='count',
            names='severity',
            title='Risk Distribution by Severity',
            color='severity',
            color_discrete_map={'High': '#ff4444', 'Medium': '#ffaa00', 'Low': '#44ff44'}
        )
        fig_severity.update_layout(
            paper_bgcolor='#0e1117',
            font=dict(color='white')
        )
        st.plotly_chart(fig_severity, use_container_width=True)
    
    # Real-time monitoring indicator
    st.markdown("---")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    <div style='text-align: center; padding: 15px; background: #1a1a2e; border-radius: 10px;'>
        <p style='color: #00d4ff; margin: 0;'>🔄 <strong>Live Monitoring Active</strong> | Last Updated: {current_time}</p>
        <p style='color: #a0a0a0; margin: 5px 0 0 0; font-size: 0.9em;'>Data refreshes every 15 minutes from weather APIs, news feeds, and port systems</p>
    </div>
    """, unsafe_allow_html=True)
