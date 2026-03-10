import streamlit as st
import plotly.graph_objects as go
import sys
from data.data_generator import generate_case_study_data, generate_supply_chain_data
from utils.translations import _

def show():
    st.title(_("📚 Tamil Nadu Case Studies"))
    st.markdown(f"**{_('Real disruption scenarios from 2023-2025 with lessons learned')}**")
    
    # Load case studies
    case_studies_df = generate_case_study_data()
    data_context = generate_supply_chain_data()
    
    company_profile = data_context.get('company_profile')
    if company_profile:
        st.info(f"🎯 **{_('Customized Context For')}**: {company_profile.get('name', 'N/A')}")
    
    # Overview
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e3a5f 0%, #2d5a7b 100%); padding: 25px; border-radius: 12px; margin: 20px 0;'>
        <h3 style='color: #00d4ff; margin-top: 0;'>{_('📖 Learning from Real Events')}</h3>
        <p style='color: white; font-size: 1.1em;'>{_("These case studies are based on actual disruptions in Tamil Nadu's supply chain ecosystem. Each demonstrates how our Control Tower would have helped predict, visualize, and mitigate the impact.")}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Case study selector
    case_titles = case_studies_df['title'].tolist()
    selected_case = st.selectbox(_("Select a case study:"), case_titles)
    
    # Get selected case study
    case = case_studies_df[case_studies_df['title'] == selected_case].iloc[0]
    
    st.markdown("---")
    
    # Case study header
    st.markdown(f"""
    <div style='background: #1a1a2e; padding: 30px; border-radius: 15px; margin: 20px 0;'>
        <h2 style='color: #00d4ff; margin-top: 0;'>{_(case['title'])}</h2>
        <p style='color: #a0a0a0; font-size: 1.1em; margin: 10px 0;'>📅 {_('Date:')} {case['date']}</p>
        <p style='color: white; font-size: 1.2em; margin: 15px 0;'>{_(case['description'])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Impact metrics
    st.markdown(f"### 📊 {_('Impact Metrics')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #ff6b6b; margin: 0; font-size: 2.5em;'>{case['actual_delay']}</h2>
            <p style='color: #a0a0a0; margin: 5px 0 0 0;'>{_('Days Delayed')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        cost_lakhs = case['actual_cost'] / 100000
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #ff6b6b; margin: 0; font-size: 2.5em;'>₹{cost_lakhs:.1f}L</h2>
            <p style='color: #a0a0a0; margin: 5px 0 0 0;'>{_('Financial Loss')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        affected_count = len(case['affected_suppliers'])
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #ffaa00; margin: 0; font-size: 2.5em;'>{affected_count}</h2>
            <p style='color: #a0a0a0; margin: 5px 0 0 0;'>{_('Suppliers Affected')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        products_count = len(case['affected_products'])
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #ffaa00; margin: 0; font-size: 2.5em;'>{products_count}</h2>
            <p style='color: #a0a0a0; margin: 5px 0 0 0;'>{_('Products Impacted')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Timeline visualization
    st.markdown(f"### ⏱️ {_('Event Timeline')}")
    
    # Create timeline based on case study
    if case['id'] == 'CS001':  # Chennai Floods
        timeline_events = [
            {'day': 0, 'event': 'Heavy rainfall warning issued', 'type': 'Warning'},
            {'day': 1, 'event': 'Chennai Port operations slowed', 'type': 'Impact'},
            {'day': 2, 'event': 'Port completely closed', 'type': 'Critical'},
            {'day': 4, 'event': 'Knitwear shipments stuck', 'type': 'Impact'},
            {'day': 6, 'event': 'Port reopened, backlog clearing', 'type': 'Recovery'},
            {'day': 10, 'event': 'Normal operations resumed', 'type': 'Recovery'}
        ]
    elif case['id'] == 'CS002':  # Thoothukudi Closure
        timeline_events = [
            {'day': 0, 'event': 'Protest announcements on social media', 'type': 'Warning'},
            {'day': 1, 'event': 'Port access blocked', 'type': 'Critical'},
            {'day': 2, 'event': 'Textile exports halted', 'type': 'Impact'},
            {'day': 3, 'event': 'Air freight arranged for urgent orders', 'type': 'Mitigation'},
            {'day': 4, 'event': 'Port access restored', 'type': 'Recovery'},
            {'day': 8, 'event': 'All delayed shipments cleared', 'type': 'Recovery'}
        ]
    else:  # US Tariff Shock
        timeline_events = [
            {'day': 0, 'event': 'Tariff announcement', 'type': 'Warning'},
            {'day': 2, 'event': 'Surge in pre-tariff orders', 'type': 'Impact'},
            {'day': 5, 'event': 'Production capacity increased', 'type': 'Mitigation'},
            {'day': 10, 'event': 'Peak production achieved', 'type': 'Recovery'},
            {'day': 15, 'event': 'Order backlog cleared', 'type': 'Recovery'}
        ]
    
    fig_timeline = go.Figure()
    
    colors = {'Warning': '#ffaa00', 'Impact': '#ff4444', 'Critical': '#cc0000', 'Mitigation': '#00d4ff', 'Recovery': '#44ff44'}
    
    for event in timeline_events:
        fig_timeline.add_trace(go.Scatter(
            x=[event['day']],
            y=[1],
            mode='markers+text',
            marker=dict(size=25, color=colors[event['type']], line=dict(width=2, color='white')),
            text=f"Day {event['day']}",
            textposition="top center",
            hovertext=f"Day {event['day']}: {event['event']}",
            hoverinfo='text',
            showlegend=False
        ))
    
    fig_timeline.update_layout(
        xaxis=dict(title=_('Days from Initial Event'), showgrid=True, gridcolor='#333'),
        yaxis=dict(showticklabels=False, showgrid=False, range=[0.5, 1.5]),
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1a1a2e',
        font=dict(color='white'),
        height=200
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Event details
    for event in timeline_events:
        timeline_string = f"Day {event['day']}: {event['event']} ({event['type']})"
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 10px 15px; border-radius: 8px; margin: 5px 0; border-left: 3px solid {colors[event['type']]};'>
            <p style='color: white; margin: 0;'>{_(timeline_string)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # What actually happened
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px;'>
            <h4 style='color: #00d4ff; margin-top: 0;'>✅ {_('Mitigation Used')}</h4>
            <p style='color: white; font-size: 1.1em;'>{_(case['mitigation_used'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px;'>
            <h4 style='color: #ffaa00; margin-top: 0;'>📚 {_('Lessons Learned')}</h4>
            <p style='color: white; font-size: 1.1em;'>{_(case['lessons'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How Control Tower would have helped
    # All case studies summary
    st.markdown("---")
    st.markdown("### 📊 All Case Studies Overview")
    
    for idx, cs in case_studies_df.iterrows():
        with st.expander(f"📁 {cs['title']} - {cs['date']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {cs['description']}")
                st.markdown(f"**Mitigation:** {cs['mitigation_used']}")
                st.markdown(f"**Lesson:** {cs['lessons']}")
            
            with col2:
                st.metric("Delay", f"{cs['actual_delay']} days")
                st.metric("Cost", f"₹{cs['actual_cost']/100000:.1f}L")
