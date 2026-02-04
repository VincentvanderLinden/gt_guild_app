"""Reusable UI components for Streamlit."""
import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime


def render_sidebar_filters(professions_list, price_data, last_update, materials_list, material_counts, company_list, company_goods_counts, last_sheet_refresh: Optional[datetime] = None, last_github_push: Optional[datetime] = None):
    """Render sidebar with filters and price info."""
    # Title at top of sidebar
    st.sidebar.markdown("<h3 style='text-align: center;'>TiT Guild App🐔™</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; font-size: 12px; color: #8b9dc3; margin-top: -10px;'>Made possible by Skunk's sheet</p>", unsafe_allow_html=True)
    
    st.sidebar.title("⚙️ Filters")
    st.sidebar.space()
    
    # Profession filter
    selected_professions = st.sidebar.multiselect(
        "Professions", 
        professions_list,
        help="Filter companies by the professions they require. Select one or more professions to narrow down results."
    )
    
    # Company filter as dropdown
    company_options = ['']  # Empty option first
    for company_name in sorted(company_list):
        goods_count = company_goods_counts.get(company_name, 0)
        if goods_count > 0:
            company_options.append(f"{company_name} ({goods_count})")
        else:
            company_options.append(company_name)
    
    selected_company_option = st.sidebar.selectbox(
        "Search Company", 
        company_options, 
        key="search_company",
        help="Filter by specific company name. Number in parentheses shows unique materials offered by that company."
    )
    
    # Extract company name without count
    if selected_company_option and '(' in selected_company_option:
        search_company = selected_company_option.rsplit(' (', 1)[0]
    else:
        search_company = selected_company_option
    
    # Search goods as dropdown with materials and counts
    material_options = ['']  # Empty option first
    for material in sorted(materials_list):
        count = material_counts.get(material, 0)
        if count > 0:
            material_options.append(f"{material} ({count})")
        else:
            material_options.append(material)
    
    selected_option = st.sidebar.selectbox(
        "Search Materials", 
        material_options, 
        key="search_goods",
        help="Filter by specific material/good. Number in parentheses shows how many companies offer this material."
    )
    
    # Extract material name without count (remove " (X)" suffix)
    if selected_option and '(' in selected_option:
        search_goods = selected_option.rsplit(' (', 1)[0]
    else:
        search_goods = selected_option
    
    # Price update status
    st.sidebar.divider()
    if price_data and last_update:
        st.sidebar.caption(f"📊 **Prices** • *{last_update}*")
    else:
        st.sidebar.caption(f"📊 **Prices** • *Not loaded*")
    
    # Google Sheets refresh status
    if last_sheet_refresh:
        time_str = last_sheet_refresh.strftime("%I:%M %p UTC")
        st.sidebar.caption(f"📋 **Sheets** • *{time_str}*")
    else:
        st.sidebar.caption(f"📋 **Sheets** • *Not synced*")
    
    # GitHub push status and button
    if last_github_push:
        time_str = last_github_push.strftime("%I:%M %p UTC")
        st.sidebar.caption(f"🌌 **GitHub** • *{time_str}*")
    else:
        st.sidebar.caption(f"🌌 **GitHub** • *Awaiting sync*")
    
    st.sidebar.divider()
    st.sidebar.markdown("")  # spacing
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
        st.metric("Total Materials", total_goods)
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
