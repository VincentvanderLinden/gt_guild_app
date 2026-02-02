"""Reusable UI components for Streamlit."""
import streamlit as st
from typing import Dict, Any


def render_sidebar_filters(professions_list, price_data, last_update):
    """Render sidebar with filters and price info."""
    st.sidebar.title("⚙️ Filters")
    st.sidebar.space()
    
    # Profession filter
    selected_professions = st.sidebar.multiselect("Professions", professions_list)
    
    # Search filters
    search_company = st.sidebar.text_input("Search Company", "", key="search_company")
    search_goods = st.sidebar.text_input("Search Goods", "", key="search_goods")
    
    # Price update status
    st.sidebar.divider()
    if price_data:
        st.sidebar.info(
            f"📊 Live prices: {len(price_data)} materials\n\n"
            f"Last updated: \n\n {last_update}\n\n*Updates every 10 minutes*"
        )
    else:
        st.sidebar.warning("⚠️ Could not load live prices")
    
    return selected_professions, search_company, search_goods


def render_stats_row(total_companies: int, total_goods: int, 
                     total_professions: int, avg_discount: float):
    """Render statistics metrics row."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Companies", total_companies)
    with col2:
        st.metric("Total Goods", total_goods)
    with col3:
        st.metric("Professions", total_professions)
    with col4:
        st.metric("Avg Discount %", f"{avg_discount:.1f}%")


def get_column_config(materials):
    """Get column configuration for data editor."""
    return {
        "Produced Goods": st.column_config.SelectboxColumn(
            "Produced Goods",
            width="medium",
            options=materials,
            required=True
        ),
        "Guildees Pay:": st.column_config.NumberColumn(
            "Guildees Pay", 
            format="$%d",
            help="Auto-calculated price after discount and bounds"
        ),
        "Live EXC Price": st.column_config.NumberColumn("Live EXC Price", format="$%d"),
        "Live AVG Price": st.column_config.NumberColumn("Live AVG Price", format="$%d"),
        "Guild Max": st.column_config.NumberColumn("Guild Max", format="$%d"),
        "Guild Min": st.column_config.NumberColumn("Guild Min", format="$%d"),
        "Guild % Discount": st.column_config.NumberColumn("Guild % Discount", format="%d %%"),
        "Guild Fixed Discount": st.column_config.NumberColumn("Guild Fixed Discount", format="$%d")
    }
