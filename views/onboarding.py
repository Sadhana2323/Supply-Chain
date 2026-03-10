import streamlit as st
import pandas as pd
from data import auth_db
from utils.translations import _

def _calc_geo_risk(location):
    """Simple helper to auto-calculate risk based on location string"""
    location = str(location).lower()
    if 'chennai' in location or 'mumbai' in location or 'coast' in location:
        return 'Flood/Cyclone-Prone'
    elif 'thoothukudi' in location or 'odisha' in location:
        return 'Cyclone-Prone'
    elif 'himalaya' in location or 'kashmir' in location:
        return 'Conflict/Landslide-Prone'
    else:
        return 'Low-Moderate Risk'

def show():
    # Read existing data if editing mode
    editing_mode = st.session_state.get('editing_mode', False)
    existing_data = {}
    if editing_mode:
        user_data = auth_db.get_user(st.session_state["username"])
        existing_data = user_data.get("company_data", {})
    
    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='font-size: 2.5em; color: #ffaa00; margin-bottom: 10px;'>{_("🏢 Comprehensive Intelligent Onboarding") if not editing_mode else _("✏️ Edit Company Profile")}</h2>
        <p style='font-size: 1.1em; color: #a0a0a0;'>{_("Configure your Supply Chain Control Tower by supplying complete node data across the 5 dimensions of resilience.") if not editing_mode else _("Update your supply chain parameters to fine-tune the Control Tower.")}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create the 5 tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        _("1. COMPANY PROFILE"), 
        _("2. SUPPLIER NETWORK"), 
        _("3. INVENTORY & WAREHOUSING"), 
        _("4. LOGISTICS NETWORK"), 
        _("5. RISK & INSIGHTS")
    ])
    
    # State tracking for data tables
    if "supplier_df" not in st.session_state:
        st.session_state.supplier_df = pd.DataFrame(
            columns=[_("Supplier Name"), _("Location (City, State)"), _("Supplier Tier"), _("Products Supplied"), _("Sourcing Type"), _("Historical Reliability (%)"), _("Lead Time (Days)"), _("Criticality")]
        )
    if "inventory_df" not in st.session_state:
        st.session_state.inventory_df = pd.DataFrame(
            columns=[_("Warehouse Location"), _("Products Stored"), _("Current Inventory Level"), _("Safety Stock Level"), _("Reorder Point"), _("Storage Capacity"), _("Is Perishable"), _("Shelf Life (Days)")]
        )
        
    # Pre-load data into DataFrames exactly ONCE when edit mode begins
    if editing_mode and st.session_state.get('load_edit_data', False):
        if "suppliers" in existing_data and existing_data["suppliers"]:
            st.session_state.supplier_df = pd.DataFrame(existing_data["suppliers"])
        if "inventory" in existing_data and existing_data["inventory"]:
            st.session_state.inventory_df = pd.DataFrame(existing_data["inventory"])
        st.session_state['load_edit_data'] = False # Prevent overwriting user's unsaved edits during reruns
    
    # Helper to safely grab keys from the profile defaults
    prof = existing_data.get("profile", {})
    logi = existing_data.get("logistics", {})
    risk = existing_data.get("risk_insights", {})
    
    # -----------------------------
    # TAB 1: COMPANY PROFILE
    # -----------------------------
    with tab1:
        st.markdown(f"### {_('Fundamental Corporate Metrics')}")
        comp_name = st.text_input(_("Company Name"), value=prof.get("name", ""))
        
        col1, col2 = st.columns(2)
        with col1:
            total_stock = st.number_input(_("Total Inventory Value (₹ Lakhs)"), min_value=0, value=prof.get("total_stock_value_lakhs", 150), step=10)
            avg_revenue = st.number_input(_("Average Monthly Revenue (₹ Lakhs)"), min_value=0, value=prof.get("avg_revenue_lakhs", 500), step=50)
            
        with col2:
            investment_opts = [_("Aggressive Growth"), _("Balanced"), _("Risk-Averse")]
            current_inv = prof.get("investment_strategy", "Balanced")
            inv_idx = investment_opts.index(current_inv) if current_inv in investment_opts else 1
            investment_risk = st.selectbox(_("Investment Strategy Focus"), investment_opts, index=inv_idx)
            
            core_prods_str = ", ".join(prof.get("core_products", ["Textiles", "Auto Components", "Raw Cotton"]))
            core_products = st.text_area(_("Core Products (Comma Separated)"), value=core_prods_str)
            
        customers_opts = [_("North America"), _("Europe"), _("Asia"), _("Middle East"), _("Africa"), _("Domestic (India)")]
        def_customers = [c for c in prof.get("key_markets", [_("North America"), _("Europe")]) if c in customers_opts]
        customers = st.multiselect(
            _("Key Customer Markets (Select Regions)"),
            customers_opts,
            default=def_customers
        )
        
    # -----------------------------
    # TAB 2: SUPPLIER NETWORK
    # -----------------------------
    with tab2:
        st.markdown(f"### {_('Supplier Node Topology')}")
        st.markdown(_("Map your critical tier 1-3 suppliers. **Geographic Risk Zone is calculated automatically by the AI Control Tower.**"))
        
        # Use data editor to allow user input
        edited_suppliers = st.data_editor(
            st.session_state.supplier_df,
            num_rows="dynamic",
            column_config={
                _("Supplier Tier"): st.column_config.SelectboxColumn(
                    _("Supplier Tier"),
                    options=[_("Tier 1 (Direct)"), _("Tier 2 (Indirect)"), _("Tier 3 (Raw Material)")]
                ),
                _("Sourcing Type"): st.column_config.SelectboxColumn(
                    _("Sourcing Type"),
                    options=[_("Single Source"), _("Multiple Source"), _("Unknown")]
                ),
                _("Historical Reliability (%)"): st.column_config.NumberColumn(
                    _("Historical Reliability (%)"), min_value=0, max_value=100, step=1
                ),
                _("Lead Time (Days)"): st.column_config.NumberColumn(
                    _("Lead Time (Days)"), min_value=1, max_value=365, step=1
                ),
                _("Criticality"): st.column_config.SelectboxColumn(
                    _("Criticality"), options=[_("Low"), _("Medium"), _("High")]
                )
            },
            use_container_width=True
        )
        
        st.session_state.supplier_df = edited_suppliers
        
        # Show what the auto-calculated risk looks like
        if not edited_suppliers.empty:
            st.markdown(f"#### {_('AI Auto-Calculated Geographic Risk Zone:')}")
            risk_df = edited_suppliers[[_("Supplier Name"), _("Location (City, State)")]].copy()
            risk_df[_("Geographic Risk Zone")] = risk_df[_("Location (City, State)")].apply(_calc_geo_risk)
            st.dataframe(risk_df, use_container_width=True)

    # -----------------------------
    # TAB 3: INVENTORY & WAREHOUSING
    # -----------------------------
    with tab3:
        st.markdown(f"### {_('Distribution Center Capacity & Shelf Life')}")
        
        # Parse products from TAB 1 to use in Tab 3 options if possible, 
        # but in Streamlit data_editor we can't easily dynamically bind multiselect options mid-flow. 
        # We will use text inputs for "Products Stored".
        
        edited_inventory = st.data_editor(
            st.session_state.inventory_df,
            num_rows="dynamic",
            column_config={
                _("Is Perishable"): st.column_config.CheckboxColumn(_("Is Perishable")),
                _("Shelf Life (Days)"): st.column_config.NumberColumn(_("Shelf Life (Days)"), min_value=1, step=1)
            },
            use_container_width=True
        )
        st.session_state.inventory_df = edited_inventory

    # -----------------------------
    # TAB 4: LOGISTICS NETWORK
    # -----------------------------
    with tab4:
        st.markdown(f"### {_('Transport, Routes & Modalities')}")
        
        all_ports = [_("Chennai"), _("Thoothukudi"), _("Krishnapatnam"), _("Cochin"), _("Mumbai"), _("Mundra")]
        col1, col2 = st.columns(2)
        with col1:
            # We map "Chennai Port" to "Chennai", etc as the user might have saved variation strings
            saved_primary = logi.get("primary_ports", [_("Chennai")])
            def_primary = [p for p in saved_primary if p in all_ports]
            if not def_primary and saved_primary: # Attempt fallback substring match
                for p in all_ports:
                   if any(p in sp for sp in saved_primary):
                       def_primary.append(p)
            primary_ports = st.multiselect(_("Primary Ports Used"), all_ports, default=def_primary)
            logistics_partners = st.text_input(_("Key Logistics Partners"), value=logi.get("partners", ""))
        with col2:
            saved_alt = logi.get("alternate_ports", [_("Thoothukudi")])
            def_alt = [p for p in saved_alt if p in all_ports]
            if not def_alt and saved_alt:
                for p in all_ports:
                   if any(p in sp for sp in saved_alt):
                       def_alt.append(p)
            alternate_ports = st.multiselect(_("Alternate Ports Available"), all_ports, default=def_alt)
            avg_freight_cost = st.number_input(_("Average Freight Cost per Container (₹)"), min_value=0, value=logi.get("avg_freight_cost", 75000), step=1000)
            
        primary_routes = st.text_area(_("Primary Shipping Routes"), value=logi.get("primary_routes", _("e.g., Chennai to Singapore, Thoothukudi to Colombo")))
        transit_times = st.text_area(_("Typical Transit Times by Route (Key-Value pairs)"), value=logi.get("transit_times", _("Chennai-Singapore: 5 Days\nThoothukudi-Colombo: 2 Days")))
        
        st.markdown(f"#### {_('Modal Split Composition (Must equal 100%)')}")
        msplit = logi.get("modal_split", {"sea": 70, "air": 10, "road": 20})
        sea_pct = st.slider(_("Sea (%)"), 0, 100, msplit.get("sea", 70))
        air_pct = st.slider(_("Air (%)"), 0, 100, msplit.get("air", 10))
        road_pct = st.slider(_("Road (%)"), 0, 100, msplit.get("road", 20))
        
        total_pct = sea_pct + air_pct + road_pct
        if total_pct != 100:
            st.error(f"⚠️ {_('Modal composition equals')} {total_pct}%. {_('It must equal precisely 100%.')}")
        else:
            st.success(_("Modal composition balanced: 100%"))

    # -----------------------------
    # TAB 5: RISK & INSIGHTS
    # -----------------------------
    with tab5:
        st.markdown(f"### {_('Exposure Indicators & Customer Liabilities')}")
        
        col1, col2 = st.columns(2)
        with col1:
            tc_val = "\n".join(risk.get("top_customers", ["US Retail Corp - ₹5Cr", "EU Importers - ₹3Cr"]))
            top_customers = st.text_area(_("Top 5 Customers by Revenue (One per line with estimate)"), value=tc_val)
            customer_locations = st.text_area(_("Customer Locations (Countries/Regions)"), value=risk.get("customer_locations", _("USA, UK, Germany")))
            late_penalty = st.text_input(_("Penalty for Late Delivery"), value=risk.get("late_penalty", _("1.5% of order value per day")))
            
            rt_opts = [_("Low - Prioritize Resilience"), _("Medium - Balanced"), _("High - Prioritize Cost Savings")]
            curr_rt = risk.get("risk_tolerance", "Medium - Balanced")
            rt_idx = rt_opts.index(curr_rt) if curr_rt in rt_opts else 1
            risk_tolerance = st.selectbox(_("Company Risk Tolerance"), rt_opts, index=rt_idx)
            
        with col2:
            sp_opts = [_("Diwali"), _("Christmas"), _("Pongal"), _("Summer"), _("Monsoon"), _("None")]
            # Extract standard peaks avoiding value errors
            def_sp = [p for p in risk.get("seasonal_peaks", [_("Christmas"), _("Diwali")]) if p in sp_opts]
            seasonal_peaks = st.multiselect(_("Seasonal Demand Peaks"), sp_opts, default=def_sp)
            
            pd_opts = [_("Floods"), _("Cyclones"), _("Port Strike"), _("Supplier Bankruptcy"), _("Cyberattack"), _("None")]
            def_pd = [p for p in risk.get("past_disruptions", [_("Floods"), _("Port Strike")]) if p in pd_opts]
            past_disruptions = st.multiselect(_("Past Disruptions Experienced"), pd_opts, default=def_pd)
            
            cm_opts = [_("Multiple Suppliers"), _("Safety Stock"), _("Alternate Ports"), _("Insurance"), _("None")]
            def_cm = [p for p in risk.get("current_mitigations", [_("Safety Stock")]) if p in cm_opts]
            current_mitigations = st.multiselect(_("Current Mitigation Strategies"), cm_opts, default=def_cm)


    # -----------------------------
    # SUBMIT BUTTON
    # -----------------------------
    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    # We disable the submit button if the logistics split isn't 100%
    can_submit = (total_pct == 100)
    
    btn_text = _("📝 Update Control Tower") if editing_mode else _("🚀 Feed Intelligence to AI Control Tower")
    submitted = st.button(btn_text, type="primary", use_container_width=True, disabled=not can_submit)
    
    if submitted:
        # Build the mega dictionary of data
        company_data = {
            "profile": {
                "name": comp_name,
                "total_stock_value_lakhs": total_stock,
                "core_products": [p.strip() for p in core_products.split(",") if p.strip()],
                "key_markets": customers,
                "avg_revenue_lakhs": avg_revenue,
                "investment_strategy": investment_risk
            },
            "suppliers": st.session_state.supplier_df.to_dict("records"),
            "inventory": st.session_state.inventory_df.to_dict("records"),
            "logistics": {
                "primary_ports": primary_ports,
                "alternate_ports": alternate_ports,
                "primary_routes": primary_routes,
                "partners": logistics_partners,
                "transit_times": transit_times,
                "modal_split": {"sea": sea_pct, "air": air_pct, "road": road_pct},
                "avg_freight_cost": avg_freight_cost
            },
            "risk_insights": {
                "top_customers": [c.strip() for c in top_customers.split("\n") if c.strip()],
                "customer_locations": customer_locations,
                "late_penalty": late_penalty,
                "seasonal_peaks": seasonal_peaks,
                "past_disruptions": past_disruptions,
                "risk_tolerance": risk_tolerance,
                "current_mitigations": current_mitigations
            }
        }
        
        username = st.session_state["username"]
        auth_db.save_company_data(username, company_data)
        
        if editing_mode:
            st.session_state["editing_mode"] = False
            st.success(_("Company Profile updated successfully! Rebuilding Live Dashboard..."))
        else:
            st.session_state["onboarded"] = True
            st.success(_("Data successfully processed by AI Matrix. Building your Live Dashboard..."))
            
        st.rerun()
