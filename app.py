import streamlit as st
import sys
from pathlib import Path

# Page configuration
st.set_page_config(page_title="Supply Chain Control Tower", layout="wide", initial_sidebar_state="expanded")

# Import views
from views import landing, risk_dashboard, dna_visualizer, cascade_simulator, whatif_optimizer, chatbot, auth, onboarding, sustainability
from utils.translations import _
from utils.role_helper import is_action_allowed

# Initialize session state for auth and lang
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'onboarded' not in st.session_state:
    st.session_state['onboarded'] = False
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en'
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = 'Admin' # Default role

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stApp {background-color: #0e1117;}
    h1, h2, h3 {color: #00d4ff;}
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a7b 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
    }
    
    /* Global Top Menu styling if needed */
    .top-menu {
        position: absolute;
        top: 15px;
        right: 25px;
        z-index: 99999;
    }

    /* ------------------------------------- */
    /* Mobile Responsiveness Rules (< 768px) */
    /* ------------------------------------- */
    @media (max-width: 768px) {
        /* Hide streamlit's native desktop sidebar toggle icon */
        [data-testid="collapsedControl"] { display: none !important; }

        /* Simplify Main Container */
        .block-container {
            padding: 4rem 1rem 1rem 1rem !important; /* Extra top padding for mobile */
            max-width: 100vw !important;
            overflow-x: hidden !important;
        }

        /* Prevent text overlapping and scaling issues */
        * {
            word-wrap: break-word !important;
            white-space: normal !important;
        }
        
        h1 { font-size: 1.8rem !important; line-height: 1.2 !important;}
        h2 { font-size: 1.4rem !important; line-height: 1.2 !important;}
        h3 { font-size: 1.2rem !important; line-height: 1.2 !important;}
        p, li, span, div, label, .stRadio { font-size: 14px !important; }

        /* Ensure accessible touch targets */
        button, .stButton>button {
            min-height: 44px !important;
            padding: 8px !important;
        }

        /* Allow Streamlit's native mobile sidebar behavior */
        section[data-testid="stSidebar"] {
            width: 80vw !important;
            max-width: 300px !important;
        }

        /* Tables and charts scroll natively */
        .js-plotly-plot, .stDataFrame, [data-testid="stTable"] {
            width: 100% !important;
            overflow-x: auto !important;
        }
        
        /* Fix Top menu overlap on mobile */
        .top-menu, div.stPopover {
            margin-bottom: 10px !important;
        }
    }
</style>
""", unsafe_allow_html=True)
# Top Bar with Profile & Language Options
col_spacer, col_menu = st.columns([8, 1])
with col_menu:
    # We use a popover container for the 3 dots
    with st.popover("⚙️ ⋮"):
        st.write(f"**{_('My Profile')}**")
        if st.session_state['username']:
            st.write(f"👤 {st.session_state['username']}")
        else:
            st.write(_("Guest"))
            
        if st.session_state.get('onboarded', False):
            st.write("---")
            st.write(f"**{_('Company Settings')}**")
            if st.button(f"✏️ {_('Edit Company Data')}", use_container_width=True):
                st.session_state['editing_mode'] = True
                st.session_state['load_edit_data'] = True
                st.rerun()

        st.write("---")
        st.write(f"**{_('Language')}**")
        lang_choice = st.radio(_("Select Locale"), ["English", "Tamil"], format_func=_, index=0 if st.session_state['lang'] == 'en' else 1, label_visibility="collapsed")
        
        new_lang = 'en' if lang_choice == "English" else 'ta'
        if new_lang != st.session_state['lang']:
            st.session_state['lang'] = new_lang
            st.rerun()
            
        st.write("---")
        st.write(f"**⚙️ {_('Access Settings')}**")
        # Radio button for Roles
        current_role_idx = ['Admin', 'Analyst', 'Viewer'].index(st.session_state.get('user_role', 'Admin'))
        role_choice = st.radio(_("Current Role"), ['Admin', 'Analyst', 'Viewer'], format_func=_, index=current_role_idx, label_visibility="collapsed")
        
        if role_choice != st.session_state.get('user_role'):
            st.session_state['user_role'] = role_choice
            st.toast(f"{_('Role switched to')} {_(role_choice)}")
            st.rerun()

# Sidebar navigation
st.sidebar.title(_("🌐 Supply Chain Control Tower"))

# Authentication Routing Logic
if not st.session_state['authenticated']:
    auth.show()
elif not st.session_state['onboarded'] or st.session_state.get('editing_mode', False):
    # User is logged in but hasn't filled out company data, or is editing it
    st.sidebar.markdown("---")
    
    if st.session_state.get('editing_mode', False):
        st.sidebar.info(_("✏️ Editing Company Data"))
        if st.sidebar.button(_("Cancel Editing")):
            st.session_state['editing_mode'] = False
            st.rerun()
    else:
        st.sidebar.warning(_("⚠️ Pending Company Setup"))
        st.sidebar.info(f"{_('User:')} {st.session_state['username']}")
    
    if st.sidebar.button(_("Logout")):
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.session_state['onboarded'] = False
        st.rerun()
        
    onboarding.show()
else:
    # Fully authenticated and onboarded
    st.sidebar.markdown("---")
    st.sidebar.success(f"👤 {st.session_state['username']}")
    
    if st.sidebar.button(_("Logout")):
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.session_state['onboarded'] = False
        st.rerun()
        
    st.sidebar.markdown("---")

    nav_emojis = {
        "Home": "🏠",
        "Live Risk Dashboard": "📊",
        "DNA Visualizer": "🧬",
        "Cascade Simulator": "⚡",
        "What-If Optimizer": "🎯",
        "Sustainability": "🌱",
        "AI Chat Assistant": "💬"
    }
    
    page_key = st.sidebar.radio(
        _("Navigate"),
        list(nav_emojis.keys()),
        format_func=lambda x: f"{nav_emojis[x]} {_(x)}"
    )
    
    # Route to pages
    if page_key == "Home":
        landing.show()
    elif page_key == "Live Risk Dashboard":
        risk_dashboard.show()
    elif page_key == "DNA Visualizer":
        dna_visualizer.show()
    elif page_key == "Cascade Simulator":
        cascade_simulator.show()
    elif page_key == "What-If Optimizer":
        whatif_optimizer.show()
    elif page_key == "Sustainability":
        sustainability.show()
    elif page_key == "AI Chat Assistant":
        chatbot.show()
