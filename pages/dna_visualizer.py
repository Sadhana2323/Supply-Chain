import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import sys
sys.path.append('..')
from data.data_generator import generate_supply_chain_data

def show():
    st.title("🧬 Supply Chain DNA Visualizer")
    st.markdown("**Interactive multi-tier supplier network with risk overlay**")
    
    # Load data
    data = generate_supply_chain_data()
    suppliers_df = data['suppliers']
    dependencies_df = data['dependencies']
    
    # Build network graph
    G = nx.DiGraph()
    
    # Add nodes
    for _, supplier in suppliers_df.iterrows():
        G.add_node(supplier['id'], **supplier.to_dict())
    
    # Add edges
    for _, dep in dependencies_df.iterrows():
        G.add_edge(dep['from'], dep['to'], **dep.to_dict())
    
    # Calculate positions using hierarchical layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Create network visualization
    st.markdown("### 🔗 Multi-Tier Supplier Network")
    
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
    
    st.plotly_chart(fig, use_container_width=True)
    
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
    st.markdown("### ⚠️ Critical Vulnerabilities Detected")
    
    # Find single source dependencies
    single_source_deps = dependencies_df[dependencies_df['single_source'] == True]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #5f1e1e 0%, #7b2d2d 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #ff4444;'>
            <h3 style='color: #ff6b6b; margin-top: 0;'>🚨 Single Points of Failure</h3>
            <p style='color: white; font-size: 1.1em;'>Found <strong>{len(single_source_deps)}</strong> critical single-source dependencies</p>
            <p style='color: #ffcccc;'>These suppliers have NO backup alternatives. If they fail, production stops immediately.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        flood_prone = len(suppliers_df[suppliers_df['risk_zone'] == 'Flood-prone'])
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #5f4a1e 0%, #7b6a2d 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #ffaa00;'>
            <h3 style='color: #ffcc66; margin-top: 0;'>🌊 Geographic Risk</h3>
            <p style='color: white; font-size: 1.1em;'><strong>{flood_prone}</strong> suppliers in flood zones</p>
            <p style='color: #ffe6cc;'>High monsoon season risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed vulnerability table
    st.markdown("### 📋 Single Source Dependencies Detail")
    
    for _, dep in single_source_deps.iterrows():
        from_supplier = suppliers_df[suppliers_df['id'] == dep['from']].iloc[0]
        to_supplier = suppliers_df[suppliers_df['id'] == dep['to']].iloc[0]
        
        st.markdown(f"""
        <div style='background: #1a1a2e; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 3px solid #ff4444;'>
            <div style='display: flex; justify-content: space-between;'>
                <div>
                    <p style='color: #ff6b6b; margin: 0; font-weight: bold;'>⚠️ {from_supplier['name']} → {to_supplier['name']}</p>
                    <p style='color: #a0a0a0; margin: 5px 0;'>Product: {dep['product']} | Lead Time: {dep['lead_time']} days</p>
                    <p style='color: #ffaa00; margin: 5px 0;'>Risk: {from_supplier['risk_zone']} zone in {from_supplier['location']}</p>
                </div>
                <div style='text-align: right;'>
                    <p style='color: #ff4444; margin: 0; font-size: 1.2em; font-weight: bold;'>HIGH RISK</p>
                    <p style='color: #a0a0a0; margin: 5px 0; font-size: 0.9em;'>No backup supplier</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 💡 Recommended Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px;'>
            <h4 style='color: #00d4ff;'>Immediate Actions (0-30 days)</h4>
            <ul style='color: white;'>
                <li>Identify backup suppliers for single-source dependencies</li>
                <li>Increase safety stock for flood-prone suppliers</li>
                <li>Set up real-time monitoring for high-risk nodes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 10px;'>
            <h4 style='color: #00d4ff;'>Strategic Actions (30-90 days)</h4>
            <ul style='color: white;'>
                <li>Diversify supplier base across geographic regions</li>
                <li>Negotiate dual-sourcing agreements</li>
                <li>Build inventory buffers for critical components</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
