"""Reusable UI components for Streamlit."""
import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime


def render_sidebar_filters(professions_list, price_data, last_update, last_sheet_refresh: Optional[datetime] = None, last_github_push: Optional[datetime] = None):
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
        st.sidebar.caption(
            f"📊 **Live prices:** {len(price_data)} materials  \n"
            f"*Last updated:*  \n"
            f"*{last_update}*  \n"
            f"*Updates every 10 minutes*"
        )
    else:
        st.sidebar.warning("⚠️ Could not load live prices")
    
    # Google Sheets refresh status
    st.sidebar.divider()
    if last_sheet_refresh:
        # Format UTC time (already in UTC from app.py)
        time_str = last_sheet_refresh.strftime("%b %d, %Y at %I:%M %p UTC")
        st.sidebar.caption(
            f"📋 **Google Sheets data**  \n"
            f"*Last refreshed:*  \n"
            f"*{time_str}*  \n"
            f"*Auto-refreshes every 10 minutes*"
        )
    else:
        st.sidebar.caption(
            f"📋 **Google Sheets data**  \n"
            f"*Not yet synced*  \n"
            f"*Will sync on next refresh*"
        )
    
    # GitHub push status and button
    st.sidebar.divider()
    if last_github_push:
        time_str = last_github_push.strftime("%b %d, %Y at %I:%M %p UTC")
        st.sidebar.caption(
            f"🌌 **Galactic Repository**  \n"
            f"*Last transmission:*  \n"
            f"*{time_str}*  \n"
            f"*Auto-sync every 2 minutes*"
        )
    else:
        st.sidebar.caption(
            f"🌌 **Galactic Repository**  \n"
            f"*Awaiting first transmission*"
        )
    
    st.sidebar.markdown("") # spacing
    st.sidebar.markdown("""
        <style>
        div.stButton > button {
            background-color: rgba(49, 51, 63, 0.2);
            color: #fafafa;
            border: 1px solid rgba(250, 250, 250, 0.2);
            transition: all 0.1s ease;
        }
        div.stButton > button:hover {
            background-color: rgba(49, 51, 63, 0.4);
            border-color: rgba(250, 250, 250, 0.4);
        }
        div.stButton > button:active {
            background-color: rgba(49, 51, 63, 0.6);
            border-color: rgba(250, 250, 250, 0.6);
            transform: translateY(1px);
        }
        </style>
    """, unsafe_allow_html=True)
    push_button = st.sidebar.button("🚀 Launch to GitHub", use_container_width=True)
    
    return selected_professions, search_company, search_goods, push_button


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


def get_column_config(materials, planets):
    """Get column configuration for data editor."""
    return {
        "Produced Goods": st.column_config.SelectboxColumn(
            "Produced Goods",
            width="medium",
            options=materials,
            required=True
        ),
        "Planet Produced": st.column_config.SelectboxColumn(
            "Planet Produced",
            width="small",
            options=planets,
            help="Planet where this good is produced"
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
