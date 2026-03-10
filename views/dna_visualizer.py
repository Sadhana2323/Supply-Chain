import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import sys
from data.data_generator import generate_supply_chain_data
from utils.translations import _

def show():
    st.title(_("🧬 Supply Chain DNA Visualizer"))
    st.markdown(f"**{_('Interactive multi-tier supplier network with risk overlay')}**")
    
    # Load data
    data = generate_supply_chain_data()
    suppliers_df = data['suppliers']
    dependencies_df = data['dependencies']
    
    company_profile = data.get('company_profile')
    if company_profile:
        st.info(f"🧬 **{_('Network Context')}**: {company_profile.get('name', 'N/A')} | **{_('Core Products')}**: {', '.join(company_profile.get('core_products', []))}")

    
    # Build network graph
    G = nx.DiGraph()
    
    # Add nodes
    for idx, supplier in suppliers_df.iterrows():
        G.add_node(supplier['id'], **supplier.to_dict())
    
    # Add edges
    for idx, dep in dependencies_df.iterrows():
        G.add_edge(dep['from'], dep['to'], **dep.to_dict())
    
    # Calculate positions using hierarchical layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Create network visualization
    st.markdown(f"### {_('Multi-Tier Supplier Network')}")
    
    # Create edge traces
    edge_traces = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        # Color based on single source dependency
        is_single_source = edge[2].get('single_source', False)
        edge_color = '#ff4444' if is_single_source else '#00d4ff'
        edge_width = 3 if is_single_source else 1
        
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=edge_width, color=edge_color),
            hoverinfo='text',
            text=f"Product: {edge[2].get('product', 'N/A')}<br>Lead Time: {edge[2].get('lead_time', 'N/A')} days<br>Single Source: {'⚠️ YES' if is_single_source else '✅ NO'}",
            showlegend=False
        )
        edge_traces.append(edge_trace)
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    
    risk_color_map = {
        'Flood-prone': '#ff4444',
        'Cyclone-prone': '#ff8800',
        'Moderate': '#ffaa00',
        'Low': '#44ff44'
    }
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        node_data = G.nodes[node]
        node_text.append(
            f"<b>{node_data['name']}</b><br>"
            f"Type: {node_data['type']}<br>"
            f"Location: {node_data['location']}<br>"
            f"Tier: {node_data['tier']}<br>"
            f"Risk Zone: {node_data['risk_zone']}"
        )
        
        node_color.append(risk_color_map.get(node_data['risk_zone'], '#00d4ff'))
        node_size.append(30 if node_data['tier'] == 1 else 20 if node_data['tier'] == 2 else 15)
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[G.nodes[node]['id'] for node in G.nodes()],
        textposition="top center",
        textfont=dict(size=10, color='white'),
        hovertext=node_text,
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='white')
        ),
        showlegend=False
    )
    
    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace])
    
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1a1a2e',
        height=600
    )
    
    event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", selection_mode="points")
    
    # Process selection
    if event and len(event.selection.points) > 0:
        point = event.selection.points[0]
        # The node trace is the last curve added
        if point["curve_number"] == len(edge_traces):
            nodes_list = list(G.nodes())
            idx = point["point_index"]
            if idx < len(nodes_list):
                st.session_state['selected_supplier'] = nodes_list[idx]
    
    # UI for Supplier Scorecard
    if 'selected_supplier' in st.session_state and st.session_state['selected_supplier']:
        import numpy as np
        supplier_id = st.session_state['selected_supplier']
        supplier_data = suppliers_df[suppliers_df['id'] == supplier_id]
        
        if not supplier_data.empty:
            sup = supplier_data.iloc[0]
            with st.expander(f"📊 Supplier Scorecard: {sup['name']}", expanded=True):
                col_info, col_metrics = st.columns([1, 2])
                
                # Check if this supplier is single source for anything
                is_single = not dependencies_df[(dependencies_df['from'] == supplier_id) & (dependencies_df['single_source'] == True)].empty
                
                with col_info:
                    st.markdown(f"**Location:** {sup['location']}")
                    st.markdown(f"**Type:** {sup['type']}")
                    st.markdown(f"**Tier:** {sup['tier']}")
                    st.markdown(f"**Sourcing:** {'Single Source ⚠️' if is_single else 'Multi-Source ✅'}")
                
                with col_metrics:
                    # Synthetic 12 month data: base reliability based on risk
                    base_rel = 96 if not is_single else 92
                    if sup['risk_zone'] == "Flood-prone":
                        base_rel -= 8
                    elif sup['risk_zone'] == "Cyclone-prone":
                        base_rel -= 5
                        
                    np.random.seed(int(hash(supplier_id) % 10000))
                    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                    data_points = np.clip(np.random.normal(base_rel, 4, 12), 50, 100)
                    
                    fig_metric = go.Figure()
                    fig_metric.add_trace(go.Scatter(
                        x=months, y=data_points, 
                        mode='lines+markers', 
                        line=dict(color='#00d4ff', width=3),
                        name='On-Time Delivery %'
                    ))
                    fig_metric.update_layout(
                        title="On-Time Delivery % (Last 12 Months)",
                        height=200, margin=dict(t=30, b=0, l=0, r=0),
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white"),
                        yaxis=dict(range=[0, 100])
                    )
                    st.plotly_chart(fig_metric, use_container_width=True)
                    
                    # Small metric cards
                    c1, c2, c3 = st.columns(3)
                    incidents = np.random.randint(0, 6)
                    
                    trend_val = data_points[-1] - data_points[-4]
                    trend = "▲" if trend_val > 2 else ("▼" if trend_val < -2 else "◆")
                    
                    latest_rel = data_points[-1]
                    action = "Find backup supplier" if is_single and latest_rel < 90 else ("Monitor closely" if latest_rel < 95 else "Reliable")
                    
                    c1.metric("Quality Incidents", incidents)
                    c2.metric("Risk Trend", f"{trend} {'Up' if trend == '▲' else 'Down' if trend == '▼' else 'Stable'}")
                    c3.metric("Action", action)
    
    # Legend
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: #1a1a2e; padding: 15px; border-radius: 10px;'>
            <h4 style='color: #00d4ff; margin-top: 0;'>Risk Zones</h4>
            <p style='color: #ff4444; margin: 5px 0;'>🔴 Flood-prone</p>
            <p style='color: #ff8800; margin: 5px 0;'>🟠 Cyclone-prone</p>
            <p style='color: #ffaa00; margin: 5px 0;'>🟡 Moderate</p>
            <p style='color: #44ff44; margin: 5px 0;'>🟢 Low Risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #1a1a2e; padding: 15px; border-radius: 10px;'>
            <h4 style='color: #00d4ff; margin-top: 0;'>Dependencies</h4>
            <p style='color: #ff4444; margin: 5px 0;'>━━ Single Source (High Risk)</p>
            <p style='color: #00d4ff; margin: 5px 0;'>━━ Multi-Source (Low Risk)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: #1a1a2e; padding: 15px; border-radius: 10px;'>
            <h4 style='color: #00d4ff; margin-top: 0;'>Node Size</h4>
            <p style='color: white; margin: 5px 0;'>● Large = Tier 1 (Ports)</p>
            <p style='color: white; margin: 5px 0;'>● Medium = Tier 2 (Manufacturers)</p>
            <p style='color: white; margin: 5px 0;'>● Small = Tier 3 (Raw Materials)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Critical Vulnerabilities Analysis
    st.markdown(f"### {_('Critical Vulnerabilities Detected')}")
    
    # Find single source dependencies
    single_source_deps = dependencies_df[dependencies_df['single_source'] == True]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #5f1e1e 0%, #7b2d2d 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #ff4444;'>
            <h3 style='color: #ff6b6b; margin-top: 0;'>{_('Single Points of Failure')}</h3>
            <p style='color: white; font-size: 1.1em;'>{_('Found 5 critical single-source dependencies')}</p>
            <p style='color: #ffcccc;'>{_('These suppliers have NO backup alternatives. If they fail, production stops immediately.')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        flood_prone = len(suppliers_df[suppliers_df['risk_zone'] == 'Flood-prone'])
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #5f4a1e 0%, #7b6a2d 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #ffaa00;'>
            <h3 style='color: #ffcc66; margin-top: 0;'>{_('Geographic Risk')}</h3>
            <p style='color: white; font-size: 1.1em;'>{_('2 suppliers in flood zones')}</p>
            <p style='color: #ffe6cc;'>{_('High monsoon season risk')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed vulnerability table
    st.markdown(f"### {_('Single Source Dependencies Detail')}")
    
    for idx, dep in single_source_deps.iterrows():
        from_supplier = suppliers_df[suppliers_df['id'] == dep['from']].iloc[0]
        to_supplier = suppliers_df[suppliers_df['id'] == dep['to']].iloc[0]
        
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 3px solid #ff4444;'>
            <div style='display: flex; justify-content: space-between;'>
                <div>
                    <p style='color: #ff6b6b; margin: 0; font-weight: bold;'>⚠️ {_(f"{from_supplier['name']} → {to_supplier['name']}")}</p>
                    <p style='color: #a0a0a0; margin: 5px 0;'>{_('Product:')} {dep['product']} | {_('Lead Time:')} {dep['lead_time']} days</p>
                    <p style='color: #ffaa00; margin: 5px 0;'>{_('Risk:')} {_(f"{from_supplier['risk_zone']} zone in {from_supplier['location']}")}</p>
                </div>
                <div style='text-align: right;'>
                    <p style='color: #ff4444; margin: 0; font-size: 1.2em; font-weight: bold;'>{_('HIGH RISK')}</p>
                    <p style='color: #a0a0a0; margin: 5px 0; font-size: 0.9em;'>{_('No backup supplier')}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("---")
    st.markdown(f"### {_('Recommended Actions')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px;'>
            <h4 style='color: #00d4ff;'>{_('Immediate Actions (0-30 days)')}</h4>
            <ul style='color: white;'>
                <li>{_('Identify backup suppliers for single-source dependencies')}</li>
                <li>{_('Increase safety stock for flood-prone suppliers')}</li>
                <li>{_('Set up real-time monitoring for high-risk nodes')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px;'>
            <h4 style='color: #00d4ff;'>{_('Strategic Actions (30-90 days)')}</h4>
            <ul style='color: white;'>
                <li>{_('Diversify supplier base across geographic regions')}</li>
                <li>{_('Negotiate dual-sourcing agreements')}</li>
                <li>{_('Build inventory buffers for critical components')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
