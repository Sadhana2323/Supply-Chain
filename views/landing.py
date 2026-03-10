import streamlit as st
from utils.translations import _

def show():
    # Hero section
    st.markdown(f"""
    <div style='text-align: center; padding: 40px 0;'>
        <h1 style='font-size: 3.5em; color: #00d4ff; margin-bottom: 10px;'>{_("🌐 AI-Powered Resilient Supply Chain Control Tower")}</h1>
        <p style='font-size: 1.3em; color: #a0a0a0;'>{_("Predict. Visualize. Optimize. Before Disruption Strikes.")}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Platform Capabilities
    st.markdown(f"<h2 style='text-align: center; color: #00d4ff; margin-top: 30px; font-weight: 300; letter-spacing: 2px;'>{_('CORE PLATFORM CAPABILITIES')}</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card' style='background: rgba(14, 17, 23, 0.7); backdrop-filter: blur(10px); padding: 30px; border-radius: 16px; margin: 15px 0; border: 1px solid rgba(255, 68, 68, 0.3); border-left: 5px solid #ff4444; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); transition: transform 0.3s ease;'>
            <div style='display: flex; align-items: center; margin-bottom: 15px;'>
                <span style='font-size: 2em; margin-right: 15px;'>📡</span>
                <h3 style='color: #ff6b6b; margin: 0; font-size: 1.5em;'>{_('Predictive Monitoring Engine')}</h3>
            </div>
            <p style='color: #e0e0e0; font-size: 1.1em; line-height: 1.6;'><strong>{_('Live Risk Dashboard:')}</strong> {_('Advanced algorithms actively scan global data streams—from extreme weather patterns to geopolitical shifts and port congestion—giving you <strong>24-72 hours advance warning</strong> before disruptions strike.')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card' style='background: rgba(14, 17, 23, 0.7); backdrop-filter: blur(10px); padding: 30px; border-radius: 16px; margin: 15px 0; border: 1px solid rgba(255, 170, 0, 0.3); border-left: 5px solid #ffaa00; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); transition: transform 0.3s ease;'>
            <div style='display: flex; align-items: center; margin-bottom: 15px;'>
                <span style='font-size: 2em; margin-right: 15px;'>🧬</span>
                <h3 style='color: #ffcc66; margin: 0; font-size: 1.5em;'>{_('Structural Vulnerability Mapping')}</h3>
            </div>
            <p style='color: #e0e0e0; font-size: 1.1em; line-height: 1.6;'><strong>{_('Supply Chain DNA Visualizer:')}</strong> {_('An interactive network topology that illuminates hidden multi-tier dependencies. Instantly identify single points of failure overlaid with localized risk data.')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='background: rgba(14, 17, 23, 0.7); backdrop-filter: blur(10px); padding: 30px; border-radius: 16px; margin: 15px 0; border: 1px solid rgba(170, 68, 255, 0.3); border-left: 5px solid #aa44ff; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); transition: transform 0.3s ease;'>
            <div style='display: flex; align-items: center; margin-bottom: 15px;'>
                <span style='font-size: 2em; margin-right: 15px;'>⚡</span>
                <h3 style='color: #cc99ff; margin: 0; font-size: 1.5em;'>{_('Ripple Effect Simulation')}</h3>
            </div>
            <p style='color: #e0e0e0; font-size: 1.1em; line-height: 1.6;'><strong>{_('Cascade Simulator:')}</strong> {_('Uncover the invisible domino effect. Simulate supplier failures to instantly generate a precise timeline predicting downstream impacts on vital customers and key products.')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card' style='background: rgba(14, 17, 23, 0.7); backdrop-filter: blur(10px); padding: 30px; border-radius: 16px; margin: 15px 0; border: 1px solid rgba(0, 212, 255, 0.3); border-left: 5px solid #00d4ff; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); transition: transform 0.3s ease;'>
            <div style='display: flex; align-items: center; margin-bottom: 15px;'>
                <span style='font-size: 2em; margin-right: 15px;'>🎯</span>
                <h3 style='color: #00d4ff; margin: 0; font-size: 1.5em;'>{_('AI-Driven Mitigation')}</h3>
            </div>
            <p style='color: #e0e0e0; font-size: 1.1em; line-height: 1.6;'><strong>{_('What-If Optimizer & AI Copilot:')}</strong> {_('Transform panic into precision. Test alternative logistical strategies to calculate the mathematical balance between optimal cost-efficiency and absolute resilience.')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Value Proposition
    st.markdown(f"<h2 style='text-align: center; color: #00d4ff; margin-top: 40px;'>{_('Why This Matters for Tamil Nadu')}</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: #1a1a2e; border-radius: 10px;'>
            <h1 style='color: #00d4ff; font-size: 3em; margin: 0;'>₹2.5Cr</h1>
            <p style='color: #a0a0a0;'>{_('Average cost of Chennai Port disruption (Dec 2023)')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: #1a1a2e; border-radius: 10px;'>
            <h1 style='color: #00d4ff; font-size: 3em; margin: 0;'>6 {_('Days')}</h1>
            <p style='color: #a0a0a0;'>{_('Average delay during monsoon season disruptions')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: #1a1a2e; border-radius: 10px;'>
            <h1 style='color: #00d4ff; font-size: 3em; margin: 0;'>40%</h1>
            <p style='color: #a0a0a0;'>{_('Cost reduction with proactive mitigation vs panic response')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Features
    st.markdown(f"<h2 style='text-align: center; color: #00d4ff; margin-top: 40px;'>{_('Powered by Advanced AI')}</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='padding: 20px; background: #1a1a2e; border-radius: 10px; text-align: center;'>
            <h3 style='color: #00d4ff;'>🤖 {_('Random Forest ML')}</h3>
            <p style='color: #a0a0a0;'>{_('Predicts disruption probability based on historical patterns, weather, and geopolitical factors')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='padding: 20px; background: #1a1a2e; border-radius: 10px; text-align: center;'>
            <h3 style='color: #00d4ff;'>🎲 {_('Monte Carlo Simulation')}</h3>
            <p style='color: #a0a0a0;'>{_('Models cascade effects with 1000+ simulations to predict cost impact range')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='padding: 20px; background: #1a1a2e; border-radius: 10px; text-align: center;'>
            <h3 style='color: #00d4ff;'>📊 {_('Network Analysis')}</h3>
            <p style='color: #a0a0a0;'>{_('Graph algorithms identify critical paths and single points of failure')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to Action
    st.markdown(f"""
    <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #1e3a5f 0%, #2d5a7b 100%); border-radius: 15px; margin-top: 30px;'>
        <h2 style='color: #00d4ff; margin-top: 0;'>🚀 {_('Ready to Explore?')}</h2>
        <p style='color: #ffffff; font-size: 1.2em;'>{_('Use the sidebar to navigate through our interactive demos')}</p>
        <p style='color: #a0a0a0; font-size: 1em;'>{_('All data is pre-loaded with Tamil Nadu context - just click and explore!')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>{_('Built for Hackathon 2025 | Tamil Nadu Supply Chain Resilience Initiative')}</p>
    </div>
    """, unsafe_allow_html=True)
