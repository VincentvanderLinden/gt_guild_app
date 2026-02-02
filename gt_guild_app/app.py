"""Main application file for TiT Guild App."""
import streamlit as st
import pandas as pd

# Import local modules
from config import APP_TITLE, APP_ICON, APP_SUBTITLE, CSS_FILE, PROFESSIONS
from data_manager import (
    load_game_materials, load_data, save_data, 
    prepare_goods_dataframe
)
from api_client import fetch_material_prices
from price_calculator import update_live_prices, calculate_all_guildees_prices
from validators import validate_goods
from stats import calculate_unique_goods, calculate_average_discount, get_unique_professions
from filters import apply_all_filters
from ui_components import render_sidebar_filters, render_stats_row, get_column_config
from api_handler import render_api_response, show_api_documentation


def initialize_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )


def load_custom_css():
    """Load and apply custom CSS."""
    with open(CSS_FILE) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'companies' not in st.session_state:
        st.session_state.companies = load_data()
    
    if 'materials' not in st.session_state:
        st.session_state.materials = load_game_materials()


def render_company_editor(company, idx, materials, price_data):
    """Render the editor interface for a single company."""
    # Format professions display
    prof_display = ', '.join(company.get('professions', [])) if company.get('professions') else company['industry']
    
    with st.expander(f"**{company['name']}** - {prof_display} | {company['timezone']} ({company['local_time']})", expanded=True):
        # Profession selector
        col_prof, col_spacer = st.columns([3, 1])
        with col_prof:
            selected_profs = st.multiselect(
                "Professions",
                options=PROFESSIONS,
                default=company.get('professions', []),
                key=f"prof_{company['name']}_{idx}"
            )
            
            # Update professions if changed
            if selected_profs != company.get('professions', []):
                for c in st.session_state.companies:
                    if c["name"] == company["name"]:
                        c["professions"] = selected_profs
                        save_data(st.session_state.companies)
                        break
        
        # Prepare goods dataframe
        goods_df = prepare_goods_dataframe(company["goods"])
        
        # Update live prices
        goods_df = update_live_prices(goods_df, price_data)
        
        # Calculate Guildees Pay
        goods_df = calculate_all_guildees_prices(goods_df)
        
        # Render data editor
        edited_goods = st.data_editor(
            goods_df,
            hide_index=True,
            width="stretch",
            num_rows="dynamic",
            key=f"table_{company['name']}_{idx}",
            disabled=["Guildees Pay:", "Live EXC Price", "Live AVG Price"],
            column_config=get_column_config(materials)
        )
        
        # Handle changes
        if not goods_df.equals(edited_goods):
            handle_goods_changes(company, edited_goods, price_data)


def handle_goods_changes(company, edited_goods, price_data):
    """Handle changes to company goods data."""
    # Validate goods
    temp_company = company.copy()
    temp_company['goods'] = edited_goods.to_dict('records')
    
    is_valid, error_msg = validate_goods(temp_company)
    
    if not is_valid:
        st.error(f"⚠️ {error_msg}")
        return
    
    # Update prices from cached data before saving
    if price_data:
        for idx, row in edited_goods.iterrows():
            material_name = row.get('Produced Goods', '')
            if material_name and material_name in price_data:
                edited_goods.at[idx, 'Live EXC Price'] = int(price_data[material_name]['currentPrice'])
                edited_goods.at[idx, 'Live AVG Price'] = int(price_data[material_name]['avgPrice'])
    
    # Update company in session state
    for c in st.session_state.companies:
        if c["name"] == company["name"]:
            c["goods"] = edited_goods.to_dict('records')
            save_data(st.session_state.companies)
            st.rerun()
            break


def main():
    """Main application logic."""
    # Setup
    initialize_page()
    initialize_session_state()
    
    # Load data
    companies = st.session_state.companies
    materials = st.session_state.materials
    
    # Check for API query parameters
    query_params = st.query_params
    
    # Handle API documentation request
    if 'api' in query_params or 'help' in query_params:
        show_api_documentation()
        return
    
    # Handle API query requests (before loading CSS to allow clean JSON output)
    if query_params and any(key in query_params for key in ['good', 'company', 'list']):
        # For API requests, we might want simpler styling
        api_handled = render_api_response(query_params, companies)
        if api_handled:
            return  # Exit early for API responses
    
    # Normal UI flow - load CSS
    load_custom_css()
    
    # Title
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.markdown(APP_SUBTITLE)
    
    # Add API info banner
    with st.expander("🔌 API Access Available", expanded=False):
        st.markdown("""
        This app supports URL parameter queries for programmatic access!
        
        **Quick Examples:**
        - `?good=Steel&format=json` - Get cheapest price for Steel
        - `?company=Flip Co&format=json` - Get all goods from a company
        - `?list=goods` - List all available goods
        - `?api` - View full API documentation
        """)
        if st.button("📖 View Full API Documentation"):
            st.query_params.update({"api": "true"})
            st.rerun()
    
    # Fetch live prices (cached for 10 minutes)
    price_data, last_update = fetch_material_prices()
    
    # Render sidebar and get filter values
    selected_professions, search_company, search_goods = render_sidebar_filters(
        PROFESSIONS, price_data, last_update
    )
    
    # Apply filters
    filtered_companies = apply_all_filters(
        companies, selected_professions, search_company, search_goods
    )
    
    # Calculate and display statistics
    total_unique_goods = calculate_unique_goods(filtered_companies)
    avg_discount = calculate_average_discount(filtered_companies)
    all_professions_used = get_unique_professions(filtered_companies)
    
    render_stats_row(
        len(filtered_companies),
        total_unique_goods,
        len(all_professions_used),
        avg_discount
    )
    
    st.divider()
    
    # Render company editors
    for idx, company in enumerate(filtered_companies):
        render_company_editor(company, idx, materials, price_data)
    
    # Footer
    st.info("💾 All changes are saved automatically")
    st.divider()
    st.write(f"**Showing {len(filtered_companies)} of {len(companies)} companies**")


if __name__ == "__main__":
    main()
