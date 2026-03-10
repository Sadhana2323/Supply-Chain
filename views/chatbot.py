import streamlit as st
import time
from utils.translations import _

def show():
    st.title(_("💬 AI Supply Chain Assistant"))
    st.markdown(f"**{_('Your intelligent copilot for supply chain resilience and risk management.')}**")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": _("Welcome to the Supply Chain Control Tower! I'm your AI Assistant. How can I help you analyze risks, optimize routes, or simulate cascades today?")}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input(_("Ask about Chennai Port status, risk exposure, or optimization strategies...")):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Simulated AI responses based on keywords
            lower_prompt = prompt.lower()
            if "chennai port" in lower_prompt or "flood" in lower_prompt:
                ai_response = "Based on our predictive models, Chennai Port is currently showing a **High Alert (🔴)** due to incoming heavy rainfall. Historical data (Dec 2023) suggests a potential 4-6 day delay. I recommend proactively routing urgent shipments through Krishnapatnam Port instead."
            elif "single point" in lower_prompt or "failure" in lower_prompt or "dependency" in lower_prompt:
                ai_response = "Analyzing the supply chain network... I've identified **3 critical single points of failure** in your current setup. The most vulnerable is Tiruppur Knitwear Exports Ltd., which relies entirely on a single dye supplier in Madurai. Check the **DNA Visualizer** for a complete breakdown."
            elif "cascade" in lower_prompt or "impact" in lower_prompt or "disruption" in lower_prompt:
                ai_response = "If Tiruppur Knitwear Exports fails today, our Monte Carlo simulation predicts it will affect 2 major US clients by Day 7, with an expected revenue impact of ₹1.2Cr. You can run detailed scenarios in the **Cascade Simulator**."
            elif "optimize" in lower_prompt or "cost" in lower_prompt or "strategy" in lower_prompt:
                ai_response = "To optimize your current situation, I recommend a mixed strategy: air freight the top 15% high-value items, and buffer inventory for the rest. This provides the best cost-resilience balance, potentially saving you 35% compared to a reactive approach. See the **What-If Optimizer** for details."
            elif "hackathon" in lower_prompt or "judge" in lower_prompt or "win" in lower_prompt:
                ai_response = "This Control Tower solution demonstrates clear, actionable AI use cases for supply chains: predictive risk modeling, graph-based visual dependency mapping, Monte Carlo cascade simulation, and LLM-powered insights. It solves multi-crore real-world problems for Tamil Nadu explicitly. I'm sure the judges will be very impressed! 🚀"
            else:
                ai_response = "I'm analyzing your request against our real-time supply chain data matrix. To see the full impact on your network, I recommend checking the Live Risk Dashboard or running a What-If Optimization."

            # Simulate stream of response
            for chunk in ai_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
