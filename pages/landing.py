import streamlit as st

def show():
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 40px 0;'>
        <h1 style='font-size: 3.5em; color: #00d4ff; margin-bottom: 10px;'>🌐 AI-Powered Resilient Supply Chain Control Tower</h1>
        <p style='font-size: 1.3em; color: #a0a0a0;'>Predict. Visualize. Optimize. Before Disruption Strikes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # The Four Problems
    st.markdown("<h2 style='text-align: center; color: #00d4ff; margin-top: 30px;'>The Four Critical Problems We Solve</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #5f1e1e 0%, #7b2d2d 100%); padding: 25px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #ff4444;'>
            <h3 style='color: #ff6b6b; margin-top: 0;'>❌ PROBLEM 1: NO WARNING SYSTEM</h3>
            <p style='color: #ffcccc; font-size: 1.05em;'><strong>Current Reality:</strong> Companies only see problems AFTER they happen. By the time Chennai Port floods, shipments are already stuck.</p>
            <hr style='border-color: #ff6b6b;'>
            <p style='color: #90EE90; font-size: 1.05em;'><strong>✅ Our Solution:</strong> <strong>Live Risk Dashboard</strong> - Real-time monitoring with weather alerts, geopolitical news, and port congestion. Color-coded risk levels (🔴 Red / 🟡 Yellow / 🟢 Green) give you 24-72 hour advance warning.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #5f4a1e 0%, #7b6a2d 100%); padding: 25px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #ffaa00;'>
            <h3 style='color: #ffcc66; margin-top: 0;'>⚠️ PROBLEM 2: HIDDEN WEAKNESSES</h3>
            <p style='color: #ffe6cc; font-size: 1.05em;'><strong>Current Reality:</strong> Companies don't know they rely on single suppliers in risky areas until it's too late. "We didn't know our cotton supplier was in a flood zone!"</p>
            <hr style='border-color: #ffcc66;'>
            <p style='color: #90EE90; font-size: 1.05em;'><strong>✅ Our Solution:</strong> <strong>Supply Chain DNA Visualizer</strong> - Interactive network graph showing multi-tier dependencies. Red highlights expose single points of failure overlaid with geographic risk data.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #4a1e5f 0%, #6a2d7b 100%); padding: 25px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #aa44ff;'>
            <h3 style='color: #cc99ff; margin-top: 0;'>⚡ PROBLEM 3: INVISIBLE DOMINO EFFECT</h3>
            <p style='color: #e6ccff; font-size: 1.05em;'><strong>Current Reality:</strong> Can't predict how one failure cascades. "If Tiruppur supplier fails, which customers are affected and when?"</p>
            <hr style='border-color: #cc99ff;'>
            <p style='color: #90EE90; font-size: 1.05em;'><strong>✅ Our Solution:</strong> <strong>Cascade Simulator</strong> - Click any supplier to see downstream impact. Shows which products, customers, and regions will be affected with precise timeline (Day 0, Day 3, Day 7).</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #1e3a5f 0%, #2d5a7b 100%); padding: 25px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #00d4ff;'>
            <h3 style='color: #66ccff; margin-top: 0;'>🎯 PROBLEM 4: PANIC MODE PLANNING</h3>
            <p style='color: #cce6ff; font-size: 1.05em;'><strong>Current Reality:</strong> Panic decisions waste money. "Should we air freight everything or wait? We're guessing!"</p>
            <hr style='border-color: #66ccff;'>
            <p style='color: #90EE90; font-size: 1.05em;'><strong>✅ Our Solution:</strong> <strong>What-If Optimizer</strong> - Test multiple strategies (air freight, alternate suppliers, inventory buffers). AI recommends optimal cost-resilience balance with clear ROI.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Value Proposition
    st.markdown("<h2 style='text-align: center; color: #00d4ff; margin-top: 40px;'>Why This Matters for Tamil Nadu</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #1a1a2e; border-radius: 10px;'>
            <h1 style='color: #00d4ff; font-size: 3em; margin: 0;'>₹2.5Cr</h1>
            <p style='color: #a0a0a0;'>Average cost of Chennai Port disruption (Dec 2023)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #1a1a2e; border-radius: 10px;'>
            <h1 style='color: #00d4ff; font-size: 3em; margin: 0;'>6 Days</h1>
            <p style='color: #a0a0a0;'>Average delay during monsoon season disruptions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #1a1a2e; border-radius: 10px;'>
            <h1 style='color: #00d4ff; font-size: 3em; margin: 0;'>40%</h1>
            <p style='color: #a0a0a0;'>Cost reduction with proactive mitigation vs panic response</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Features
    st.markdown("<h2 style='text-align: center; color: #00d4ff; margin-top: 40px;'>Powered by Advanced AI</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='padding: 20px; background: #1a1a2e; border-radius: 10px; text-align: center;'>
            <h3 style='color: #00d4ff;'>🤖 Random Forest ML</h3>
            <p style='color: #a0a0a0;'>Predicts disruption probability based on historical patterns, weather, and geopolitical factors</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='padding: 20px; background: #1a1a2e; border-radius: 10px; text-align: center;'>
            <h3 style='color: #00d4ff;'>🎲 Monte Carlo Simulation</h3>
            <p style='color: #a0a0a0;'>Models cascade effects with 1000+ simulations to predict cost impact range</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='padding: 20px; background: #1a1a2e; border-radius: 10px; text-align: center;'>
            <h3 style='color: #00d4ff;'>📊 Network Analysis</h3>
            <p style='color: #a0a0a0;'>Graph algorithms identify critical paths and single points of failure</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to Action
    st.markdown("""
    <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #1e3a5f 0%, #2d5a7b 100%); border-radius: 15px; margin-top: 30px;'>
        <h2 style='color: #00d4ff; margin-top: 0;'>🚀 Ready to Explore?</h2>
        <p style='color: #ffffff; font-size: 1.2em;'>Use the sidebar to navigate through our interactive demos</p>
        <p style='color: #a0a0a0; font-size: 1em;'>All data is pre-loaded with Tamil Nadu context - just click and explore!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Built for Hackathon 2025 | Tamil Nadu Supply Chain Resilience Initiative</p>
    </div>
    """, unsafe_allow_html=True)
