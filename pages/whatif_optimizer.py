import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys
sys.path.append('..')
from data.data_generator import generate_supply_chain_data
from models.ml_models import WhatIfOptimizer

def show():
    st.title("🎯 What-If Scenario Optimizer")
    st.markdown("**Test multiple response strategies and find the optimal cost-resilience balance**")
    
    # Load data
    data = generate_supply_chain_data()
    products_df = data['products']
    
    # Initialize optimizer
    optimizer = WhatIfOptimizer(products_df)
    
    # Scenario configuration
    st.markdown("### ⚙️ Configure Disruption Scenario")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        delay_days = st.slider("Expected Delay (days)", 1, 21, 7, help="How many days will the disruption last?")
    
    with col2:
        supplier_failure_prob = st.slider("Supplier Failure Probability", 0.0, 1.0, 0.5, 0.1, help="Likelihood of supplier completely failing")
    
    with col3:
        demand_spike_pct = st.slider("Demand Spike (%)", 0, 100, 20, 5, help="Unexpected increase in customer demand")
    
    st.markdown(f"""
    <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; margin: 20px 0;'>
        <h4 style='color: #00d4ff; margin-top: 0;'>Scenario Summary</h4>
        <p style='color: white; margin: 5px 0;'>A <strong>{delay_days}-day</strong> disruption with <strong>{supplier_failure_prob*100:.0f}%</strong> chance of complete supplier failure and <strong>{demand_spike_pct}%</strong> demand increase</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Run optimization
    if st.button("🚀 Optimize Strategy", type="primary"):
        with st.spinner("Analyzing strategies and calculating optimal response..."):
            result = optimizer.optimize_strategy(delay_days, supplier_failure_prob, demand_spike_pct)
        
        st.session_state['optimization_result'] = result
    
    # Display results
    if 'optimization_result' in st.session_state:
        result = st.session_state['optimization_result']
        
        st.markdown("---")
        st.markdown("### 📊 Strategy Comparison")
        
        # Baseline cost
        baseline_cr = result['baseline_cost'] / 10000000
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #5f1e1e 0%, #7b2d2d 100%); padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;'>
            <h3 style='color: #ff6b6b; margin: 0;'>Baseline Cost (Do Nothing)</h3>
            <h1 style='color: white; margin: 10px 0; font-size: 3em;'>₹{baseline_cr:.2f} Cr</h1>
            <p style='color: #ffcccc; margin: 0;'>Total revenue loss if no action is taken</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Strategy cards
        st.markdown("### 🎯 Available Strategies")
        
        strategies = result['strategies']
        
        for i, strategy in enumerate(strategies):
            cost_cr = strategy['cost'] / 10000000
            savings = result['baseline_cost'] - strategy['cost']
            savings_pct = (savings / result['baseline_cost']) * 100
            
            # Color based on rank
            if i == 0:
                border_color = "#44ff44"
                badge = "⭐ RECOMMENDED"
                badge_color = "#44ff44"
            else:
                border_color = "#00d4ff"
                badge = ""
                badge_color = "#00d4ff"
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style='background: #1a1a2e; padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 5px solid {border_color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h3 style='color: {badge_color}; margin: 0;'>{strategy['name']} {badge}</h3>
                            <p style='color: #a0a0a0; margin: 10px 0;'>{strategy['description']}</p>
                            <p style='color: white; margin: 5px 0;'>Implementation Time: <strong>{strategy['implementation_time']}</strong></p>
                            <p style='color: white; margin: 5px 0;'>Resilience Score: <strong>{strategy['resilience_score']*100:.0f}%</strong></p>
                        </div>
                        <div style='text-align: right;'>
                            <h2 style='color: {badge_color}; margin: 0;'>₹{cost_cr:.2f}Cr</h2>
                            <p style='color: #44ff44; margin: 5px 0;'>Save ₹{savings/10000000:.2f}Cr</p>
                            <p style='color: #a0a0a0; margin: 5px 0; font-size: 0.9em;'>({savings_pct:.1f}% reduction)</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Resilience gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=strategy['resilience_score'] * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': border_color},
                        'bgcolor': "#1a1a2e",
                        'borderwidth': 2,
                        'bordercolor': "white",
                        'steps': [
                            {'range': [0, 50], 'color': '#ff4444'},
                            {'range': [50, 75], 'color': '#ffaa00'},
                            {'range': [75, 100], 'color': '#44ff44'}
                        ]
                    }
                ))
                fig.update_layout(
                    paper_bgcolor='#0e1117',
                    font={'color': "white", 'size': 12},
                    height=150,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Comparison chart
        st.markdown("---")
        st.markdown("### 📈 Cost vs Resilience Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cost comparison bar chart
            strategy_names = [s['name'] for s in strategies]
            strategy_costs = [s['cost'] / 10000000 for s in strategies]
            
            fig_cost = go.Figure(data=[
                go.Bar(
                    x=strategy_names,
                    y=strategy_costs,
                    marker_color=['#44ff44' if i == 0 else '#00d4ff' for i in range(len(strategies))],
                    text=[f"₹{c:.2f}Cr" for c in strategy_costs],
                    textposition='auto'
                )
            ])
            
            fig_cost.add_hline(y=baseline_cr, line_dash="dash", line_color="#ff4444", 
                              annotation_text="Baseline (Do Nothing)", annotation_position="right")
            
            fig_cost.update_layout(
                title="Total Cost Comparison",
                xaxis_title="Strategy",
                yaxis_title="Cost (₹ Crores)",
                paper_bgcolor='#0e1117',
                plot_bgcolor='#1a1a2e',
                font=dict(color='white'),
                showlegend=False
            )
            
            st.plotly_chart(fig_cost, use_container_width=True)
        
        with col2:
            # Resilience comparison
            strategy_resilience = [s['resilience_score'] * 100 for s in strategies]
            
            fig_resilience = go.Figure(data=[
                go.Bar(
                    x=strategy_names,
                    y=strategy_resilience,
                    marker_color=['#44ff44' if i == 0 else '#00d4ff' for i in range(len(strategies))],
                    text=[f"{r:.0f}%" for r in strategy_resilience],
                    textposition='auto'
                )
            ])
            
            fig_resilience.update_layout(
                title="Resilience Score Comparison",
                xaxis_title="Strategy",
                yaxis_title="Resilience Score (%)",
                paper_bgcolor='#0e1117',
                plot_bgcolor='#1a1a2e',
                font=dict(color='white'),
                showlegend=False
            )
            
            st.plotly_chart(fig_resilience, use_container_width=True)
        
        # Scatter plot: Cost vs Resilience
        st.markdown("### 🎯 Optimal Strategy Selection")
        
        fig_scatter = go.Figure()
        
        for i, strategy in enumerate(strategies):
            is_recommended = i == 0
            fig_scatter.add_trace(go.Scatter(
                x=[strategy['cost'] / 10000000],
                y=[strategy['resilience_score'] * 100],
                mode='markers+text',
                marker=dict(
                    size=30 if is_recommended else 20,
                    color='#44ff44' if is_recommended else '#00d4ff',
                    line=dict(width=3 if is_recommended else 1, color='white')
                ),
                text=strategy['name'],
                textposition="top center",
                name=strategy['name'],
                hovertext=f"{strategy['name']}<br>Cost: ₹{strategy['cost']/10000000:.2f}Cr<br>Resilience: {strategy['resilience_score']*100:.0f}%",
                hoverinfo='text'
            ))
        
        fig_scatter.update_layout(
            title="Cost-Resilience Trade-off (Lower-Left is Better)",
            xaxis_title="Total Cost (₹ Crores)",
            yaxis_title="Resilience Score (%)",
            paper_bgcolor='#0e1117',
            plot_bgcolor='#1a1a2e',
            font=dict(color='white'),
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Final recommendation
        recommended = result['recommended']
        savings = result['baseline_cost'] - recommended['cost']
        savings_pct = (savings / result['baseline_cost']) * 100
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1e5f1e 0%, #2d7b2d 100%); padding: 30px; border-radius: 15px; margin: 30px 0; border: 3px solid #44ff44;'>
            <h2 style='color: #44ff44; margin-top: 0; text-align: center;'>⭐ RECOMMENDED STRATEGY</h2>
            <h1 style='color: white; text-align: center; font-size: 2.5em; margin: 20px 0;'>{recommended['name']}</h1>
            <div style='display: flex; justify-content: space-around; margin: 20px 0;'>
                <div style='text-align: center;'>
                    <h3 style='color: white; margin: 0;'>₹{recommended['cost']/10000000:.2f} Cr</h3>
                    <p style='color: #ccffcc; margin: 5px 0;'>Total Cost</p>
                </div>
                <div style='text-align: center;'>
                    <h3 style='color: white; margin: 0;'>{recommended['resilience_score']*100:.0f}%</h3>
                    <p style='color: #ccffcc; margin: 5px 0;'>Resilience</p>
                </div>
                <div style='text-align: center;'>
                    <h3 style='color: white; margin: 0;'>₹{savings/10000000:.2f} Cr</h3>
                    <p style='color: #ccffcc; margin: 5px 0;'>Savings ({savings_pct:.1f}%)</p>
                </div>
            </div>
            <p style='color: white; text-align: center; font-size: 1.1em; margin: 20px 0;'>{recommended['description']}</p>
            <p style='color: #ccffcc; text-align: center;'>Implementation Time: <strong>{recommended['implementation_time']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.info("👆 Configure your scenario and click 'Optimize Strategy' to see recommendations")
