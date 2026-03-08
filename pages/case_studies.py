import streamlit as st
import plotly.graph_objects as go
import sys
sys.path.append('..')
from data.data_generator import generate_case_study_data

def show():
    st.title("📚 Tamil Nadu Case Studies")
    st.markdown("**Real disruption scenarios from 2023-2025 with lessons learned**")
    
    # Load case studies
    case_studies_df = generate_case_study_data()
    
    # Overview
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e3a5f 0%, #2d5a7b 100%); padding: 25px; border-radius: 12px; margin: 20px 0;'>
        <h3 style='color: #00d4ff; margin-top: 0;'>📖 Learning from Real Events</h3>
        <p style='color: white; font-size: 1.1em;'>These case studies are based on actual disruptions in Tamil Nadu's supply chain ecosystem. Each demonstrates how our Control Tower would have helped predict, visualize, and mitigate the impact.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Case study selector
    case_titles = case_studies_df['title'].tolist()
    selected_case = st.selectbox("Select a case study:", case_titles)
    
    # Get selected case study
    case = case_studies_df[case_studies_df['title'] == selected_case].iloc[0]
    
    st.markdown("---")
    
    # Case study header
    st.markdown(f"""
    <div style='background: #1a1a2e; padding: 30px; border-radius: 15px; margin: 20px 0;'>
        <h2 style='color: #00d4ff; margin-top: 0;'>{case['title']}</h2>
        <p style='color: #a0a0a0; font-size: 1.1em; margin: 10px 0;'>📅 Date: {case['date']}</p>
        <p style='color: white; font-size: 1.2em; margin: 15px 0;'>{case['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Impact metrics
    st.markdown("### 📊 Impact Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #ff6b6b; margin: 0; font-size: 2.5em;'>{case['actual_delay']}</h2>
            <p style='color: #a0a0a0; margin: 5px 0 0 0;'>Days Delayed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        cost_lakhs = case['actual_cost'] / 100000
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #ff6b6b; margin: 0; font-size: 2.5em;'>₹{cost_lakhs:.1f}L</h2>
            <p style='color: #a0a0a0; margin: 5px 0 0 0;'>Financial Loss</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        affected_count = len(case['affected_suppliers'].split(','))
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #ffaa00; margin: 0; font-size: 2.5em;'>{affected_count}</h2>
            <p style='color: #a0a0a0; margin: 5px 0 0 0;'>Suppliers Affected</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        products_count = len(case['affected_products'].split(','))
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #ffaa00; margin: 0; font-size: 2.5em;'>{products_count}</h2>
            <p style='color: #a0a0a0; margin: 5px 0 0 0;'>Products Impacted</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Timeline visualization
    st.markdown("### ⏱️ Event Timeline")
    
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
        xaxis=dict(title='Days from Initial Event', showgrid=True, gridcolor='#333'),
        yaxis=dict(showticklabels=False, showgrid=False, range=[0.5, 1.5]),
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1a1a2e',
        font=dict(color='white'),
        height=200
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Event details
    for event in timeline_events:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 10px 15px; border-radius: 8px; margin: 5px 0; border-left: 3px solid {colors[event['type']]};'>
            <p style='color: white; margin: 0;'><strong>Day {event['day']}:</strong> {event['event']} <span style='color: {colors[event['type']]};'>({event['type']})</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # What actually happened
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px;'>
            <h4 style='color: #00d4ff; margin-top: 0;'>✅ Mitigation Used</h4>
            <p style='color: white; font-size: 1.1em;'>{case['mitigation_used']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px;'>
            <h4 style='color: #ffaa00; margin-top: 0;'>📚 Lessons Learned</h4>
            <p style='color: white; font-size: 1.1em;'>{case['lessons']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How Control Tower would have helped
    st.markdown("### 🌐 How Our Control Tower Would Have Helped")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1e5f1e 0%, #2d7b2d 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #44ff44;'>
            <h4 style='color: #44ff44; margin-top: 0;'>🔴 PROBLEM 1: Early Warning</h4>
            <p style='color: white;'><strong>Without Control Tower:</strong> Learned about disruption when it happened</p>
            <p style='color: #ccffcc;'><strong>With Control Tower:</strong> 24-48 hour advance warning from weather/news monitoring would have allowed proactive rerouting</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1e5f1e 0%, #2d7b2d 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #44ff44;'>
            <h4 style='color: #44ff44; margin-top: 0;'>🟡 PROBLEM 2: Hidden Dependencies</h4>
            <p style='color: white;'><strong>Without Control Tower:</strong> Didn't realize single-port dependency until too late</p>
            <p style='color: #ccffcc;'><strong>With Control Tower:</strong> DNA Visualizer would have shown single-point-of-failure risk months earlier</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1e5f1e 0%, #2d7b2d 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #44ff44;'>
            <h4 style='color: #44ff44; margin-top: 0;'>🟣 PROBLEM 3: Cascade Prediction</h4>
            <p style='color: white;'><strong>Without Control Tower:</strong> Discovered downstream impacts day-by-day as they happened</p>
            <p style='color: #ccffcc;'><strong>With Control Tower:</strong> Cascade Simulator would have predicted all affected customers and timeline immediately</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1e5f1e 0%, #2d7b2d 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #44ff44;'>
            <h4 style='color: #44ff44; margin-top: 0;'>🔵 PROBLEM 4: Optimal Response</h4>
            <p style='color: white;'><strong>Without Control Tower:</strong> Made reactive decisions under pressure</p>
            <p style='color: #ccffcc;'><strong>With Control Tower:</strong> What-If Optimizer would have recommended optimal strategy saving 30-40% of costs</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Potential savings calculation
    st.markdown("---")
    st.markdown("### 💰 Potential Savings with Control Tower")
    
    potential_savings = case['actual_cost'] * 0.35  # 35% savings estimate
    faster_recovery = max(1, case['actual_delay'] - 2)  # 2 days faster
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: #ff6b6b; margin: 0;'>₹{case['actual_cost']/100000:.1f}L</h3>
            <p style='color: #a0a0a0; margin: 5px 0;'>Actual Cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: #44ff44; margin: 0;'>₹{(case['actual_cost']-potential_savings)/100000:.1f}L</h3>
            <p style='color: #a0a0a0; margin: 5px 0;'>Estimated with Control Tower</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1e5f1e 0%, #2d7b2d 100%); padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: #44ff44; margin: 0;'>₹{potential_savings/100000:.1f}L</h3>
            <p style='color: white; margin: 5px 0;'>Potential Savings (35%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center;'>
        <p style='color: white; font-size: 1.2em; margin: 0;'>Recovery time could have been reduced from <strong>{case['actual_delay']} days</strong> to <strong>{faster_recovery} days</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # All case studies summary
    st.markdown("---")
    st.markdown("### 📊 All Case Studies Overview")
    
    for _, cs in case_studies_df.iterrows():
        with st.expander(f"📁 {cs['title']} - {cs['date']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {cs['description']}")
                st.markdown(f"**Mitigation:** {cs['mitigation_used']}")
                st.markdown(f"**Lesson:** {cs['lessons']}")
            
            with col2:
                st.metric("Delay", f"{cs['actual_delay']} days")
                st.metric("Cost", f"₹{cs['actual_cost']/100000:.1f}L")
