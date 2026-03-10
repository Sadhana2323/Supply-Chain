import streamlit as st
from data import auth_db
from utils.translations import _

def show():
    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 3em; color: #00d4ff; margin-bottom: 10px;'>{_("🌐 Supply Chain Control Tower")}</h1>
        <p style='font-size: 1.2em; color: #a0a0a0;'>{_("Log in or create an account to access real-time risk intelligence.")}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs([_("Login"), _("Sign Up")])
        
        with tab1:
            st.markdown(f"### {_('Welcome Back')}")
            login_user = st.text_input(_("Username"), key="login_user")
            login_pass = st.text_input(_("Password"), type="password", key="login_pass")
            
            if st.button(_("Log In"), type="primary", use_container_width=True):
                if auth_db.authenticate_user(login_user, login_pass):
                    user_data = auth_db.get_user(login_user)
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = login_user
                    st.session_state["onboarded"] = user_data.get("onboarded", False)
                    st.success(_("Login successful! Redirecting..."))
                    st.rerun()
                else:
                    st.error(_("Invalid username or password."))
        
        with tab2:
            st.markdown(f"### {_('Create an Account')}")
            reg_email = st.text_input(_("Email"), key="reg_email")
            reg_user = st.text_input(_("Username"), key="reg_user")
            reg_pass = st.text_input(_("Password"), type="password", key="reg_pass")
            reg_pass_confirm = st.text_input(_("Confirm Password"), type="password", key="reg_pass_confirm")
            
            if st.button(_("Sign Up"), type="primary", use_container_width=True):
                if reg_pass != reg_pass_confirm:
                    st.error(_("Passwords do not match."))
                elif len(reg_user) < 3 or len(reg_pass) < 4:
                    st.error(_("Username must be at least 3 characters and password at least 4 characters."))
                else:
                    success = auth_db.create_user(reg_user, reg_pass, reg_email)
                    if success:
                        st.success(_("Account created successfully! Please log in."))
                    else:
                        st.error(_("Username already exists. Please choose another."))
