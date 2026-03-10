import streamlit as st

def is_action_allowed(action_level):
    """
    Check if the current user role has permission to perform an action.
    - 'Admin': Full access (simulate, optimize, edit)
    - 'Analyst': Can simulate and optimize, but cannot edit core data
    - 'Viewer': Cannot simulate, optimize, or edit
    """
    # Default to Viewer if not set
    role = st.session_state.get('user_role', 'Viewer')
    
    if role == 'Admin':
        return True
    
    if role == 'Analyst':
        if action_level in ['simulate', 'optimize']:
            return True
        return False
        
    if role == 'Viewer':
        return False
        
    return False
