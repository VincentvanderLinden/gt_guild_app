"""Main application file for TiT Guild App."""
import streamlit as st
import pandas as pd

# Import local modules
from config import APP_TITLE, APP_ICON, APP_SUBTITLE, CSS_FILE, PROFESSIONS, GOOGLE_SHEET_URL, TIMEZONE_OPTIONS, TIMEZONE_OPTIONS
from core.data_manager import (
    load_game_materials, load_game_planets, load_data, save_data, 
    save_google_sheets_data, prepare_goods_dataframe, load_google_sheets_data
)
from integrations.api_client import fetch_material_prices
from business.price_calculator import update_live_prices, calculate_all_guildees_prices
from core.validators import validate_goods
from business.stats import calculate_unique_goods, calculate_average_discount, get_unique_professions
from business.filters import apply_all_filters
from ui.ui_components import render_sidebar_filters, render_stats_row, get_column_config
from integrations.timezone_utils import update_company_local_times, get_local_time, get_local_time
from integrations.google_sheets import import_from_google_sheet
from datetime import datetime, timedelta, timezone


# ============================================================================
# API Route Handlers (for Starlette integration)
# ============================================================================

async def api_health(request):
    """Health check endpoint."""
    from starlette.responses import JSONResponse
    return JSONResponse({
        "status": "healthy",
        "service": "TiT Guild App API"
    })


async def api_goods_list(request):
    """Get list of all goods across all companies."""
    from starlette.responses import JSONResponse
    companies = load_google_sheets_data()
    if not companies:
        return JSONResponse({
            "status": "error",
            "message": "No data available"
        }, status_code=404)
    
    goods_set = set()
    for company in companies:
        for good in company['goods']:
            goods_set.add(good.get('Produced Goods', ''))
    
    return JSONResponse({
        "status": "success",
        "data": {
            "goods": sorted(list(goods_set)),
            "count": len(goods_set)
        }
    })


async def api_companies_list(request):
    """Get list of all companies."""
    from starlette.responses import JSONResponse
    companies = load_google_sheets_data()
    if not companies:
        return JSONResponse({
            "status": "error",
            "message": "No data available"
        }, status_code=404)
    
    company_list = []
    for company in companies:
        company_list.append({
            "name": company['name'],
            "industry": company['industry'],
            "professions": company.get('professions', []),
            "timezone": company.get('timezone', 'UTC +00:00'),
            "goods_count": len(company['goods'])
        })
    
    return JSONResponse({
        "status": "success",
        "data": {
            "companies": company_list,
            "count": len(company_list)
        }
    })


async def api_good_detail(request):
    """Get pricing details for a specific good."""
    from starlette.responses import JSONResponse
    good_name = request.path_params.get('good_name')
    if not good_name:
        return JSONResponse({
            "status": "error",
            "message": "Good name is required"
        }, status_code=400)
    
    companies = load_google_sheets_data()
    if not companies:
        return JSONResponse({
            "status": "error",
            "message": "No data available"
        }, status_code=404)
    
    results = []
    for company in companies:
        for good in company['goods']:
            if good.get('Produced Goods', '').lower() == good_name.lower():
                results.append({
                    'company': company['name'],
                    'good': good.get('Produced Goods', ''),
                    'planet_produced': good.get('Planet Produced', ''),
                    'guildees_pay': good.get('Guildees Pay:', 0),
                    'live_exc_price': good.get('Live EXC Price', 0),
                    'live_avg_price': good.get('Live AVG Price', 0),
                    'guild_max': good.get('Guild Max', 0),
                    'guild_min': good.get('Guild Min', 0),
                    'discount_percent': good.get('Guild % Discount', 0),
                    'discount_fixed': good.get('Guild Fixed Discount', 0),
                    'timezone': company.get('timezone', 'UTC +00:00'),
                    'professions': company.get('professions', [])
                })
    
    if not results:
        return JSONResponse({
            "status": "error",
            "message": f"Good '{good_name}' not found"
        }, status_code=404)
    
    results.sort(key=lambda x: x['guildees_pay'])
    
    return JSONResponse({
        "status": "success",
        "query": {"good": good_name},
        "data": {
            "results": results,
            "count": len(results),
            "cheapest": results[0] if results else None
        }
    })


async def api_company_detail(request):
    """Get details for a specific company."""
    from starlette.responses import JSONResponse
    company_name = request.path_params.get('company_name')
    if not company_name:
        return JSONResponse({
            "status": "error",
            "message": "Company name is required"
        }, status_code=400)
    
    companies = load_google_sheets_data()
    if not companies:
        return JSONResponse({
            "status": "error",
            "message": "No data available"
        }, status_code=404)
    
    for company in companies:
        if company['name'].lower() == company_name.lower():
            goods_list = []
            for good in company['goods']:
                goods_list.append({
                    'produced_goods': good.get('Produced Goods', ''),
                    'planet_produced': good.get('Planet Produced', ''),
                    'guildees_pay': good.get('Guildees Pay:', 0),
                    'live_exc_price': good.get('Live EXC Price', 0),
                    'live_avg_price': good.get('Live AVG Price', 0),
                    'guild_max': good.get('Guild Max', 0),
                    'guild_min': good.get('Guild Min', 0),
                    'discount_percent': good.get('Guild % Discount', 0),
                    'discount_fixed': good.get('Guild Fixed Discount', 0)
                })
            
            return JSONResponse({
                "status": "success",
                "query": {"company": company_name},
                "data": {
                    "name": company['name'],
                    "industry": company['industry'],
                    "professions": company.get('professions', []),
                    "timezone": company.get('timezone', 'UTC +00:00'),
                    "local_time": company.get('local_time', 'N/A'),
                    "goods": goods_list
                }
            })
    
    return JSONResponse({
        "status": "error",
        "message": f"Company '{company_name}' not found"
    }, status_code=404)


async def api_all_data(request):
    """Get complete dataset."""
    from starlette.responses import JSONResponse
    companies = load_google_sheets_data()
    if not companies:
        return JSONResponse({
            "status": "error",
            "message": "No data available"
        }, status_code=404)
    
    formatted_companies = []
    for company in companies:
        goods_list = []
        for good in company['goods']:
            goods_list.append({
                'produced_goods': good.get('Produced Goods', ''),
                'planet_produced': good.get('Planet Produced', ''),
                'guildees_pay': good.get('Guildees Pay:', 0),
                'live_exc_price': good.get('Live EXC Price', 0),
                'live_avg_price': good.get('Live AVG Price', 0),
                'guild_max': good.get('Guild Max', 0),
                'guild_min': good.get('Guild Min', 0),
                'discount_percent': good.get('Guild % Discount', 0),
                'discount_fixed': good.get('Guild Fixed Discount', 0)
            })
        
        formatted_companies.append({
            "name": company['name'],
            "industry": company['industry'],
            "professions": company.get('professions', []),
            "timezone": company.get('timezone', 'UTC +00:00'),
            "local_time": company.get('local_time', 'N/A'),
            "goods": goods_list
        })
    
    return JSONResponse({
        "status": "success",
        "data": {
            "companies": formatted_companies,
            "count": len(formatted_companies)
        }
    })


# ============================================================================
# Streamlit UI Functions
# ============================================================================

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
        # Update local times on load
        if st.session_state.companies:
            st.session_state.companies = update_company_local_times(st.session_state.companies)
    
    if 'materials' not in st.session_state:
        st.session_state.materials = load_game_materials()
    
    if 'planets' not in st.session_state:
        st.session_state.planets = load_game_planets()
    
    if 'last_sheet_refresh' not in st.session_state:
        st.session_state.last_sheet_refresh = None
    
    if 'sheet_url' not in st.session_state:
        st.session_state.sheet_url = GOOGLE_SHEET_URL


def refresh_from_google_sheets():
    """Refresh data from Google Sheets if 10 minutes have passed."""
    now = datetime.now(timezone.utc)
    
    # Check if we need to refresh (10 minutes = 600 seconds)
    if st.session_state.last_sheet_refresh is None or \
       (now - st.session_state.last_sheet_refresh) > timedelta(minutes=10):
        
        try:
            # Import from Google Sheets
            companies = import_from_google_sheet(st.session_state.sheet_url)
            
            if companies:
                # Update local times
                companies = update_company_local_times(companies)
                
                # Save to main data file only
                # google_sheets_data will be saved when prices are calculated
                save_data(companies)
                
                # Update session state
                st.session_state.companies = companies
                st.session_state.last_sheet_refresh = now
                
                return True
        except Exception as e:
            print(f"Error refreshing from Google Sheets: {e}")
            return False
    
    return False


def render_company_editor(company, idx, materials, price_data, all_professions_list, search_goods=""):
    """Render the editor interface for a single company."""
    # Format professions display
    prof_display = ', '.join(company.get('professions', [])) if company.get('professions') else company['industry']
    
    with st.expander(f"**{company['name']}** - {prof_display} | {company['timezone']} ({company['local_time']})", expanded=True):
        # Profession and Timezone selectors
        col_prof, col_tz = st.columns([3, 3])
        with col_prof:
            selected_profs = st.multiselect(
                "Professions",
                options=all_professions_list,
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
        
        with col_tz:
            # Extract just the UTC offset from current timezone for matching
            current_tz = company.get('timezone', 'UTC +00:00')
            # Find matching option or default to current value
            try:
                current_idx = next((i for i, opt in enumerate(TIMEZONE_OPTIONS) if current_tz.split('(')[0].strip() in opt), None)
                if current_idx is None:
                    # If current timezone not in list, add it as first option
                    timezone_opts = [current_tz] + TIMEZONE_OPTIONS
                    current_idx = 0
                else:
                    timezone_opts = TIMEZONE_OPTIONS
            except:
                timezone_opts = TIMEZONE_OPTIONS
                current_idx = 12  # Default to UTC +00:00
            
            selected_tz = st.selectbox(
                "Timezone",
                options=timezone_opts,
                index=current_idx,
                key=f"tz_{company['name']}_{idx}"
            )
            
            # Extract just UTC offset part (e.g., "UTC +01:00" from "UTC +01:00 (Paris, Berlin)")
            tz_offset = selected_tz.split('(')[0].strip()
            
            # Update timezone if changed
            if tz_offset != current_tz:
                for c in st.session_state.companies:
                    if c["name"] == company["name"]:
                        c["timezone"] = tz_offset
                        # Update local time immediately
                        c['local_time'] = get_local_time(tz_offset)
                        save_data(st.session_state.companies)
                        save_google_sheets_data(st.session_state.companies)
                        break
        
        # Prepare goods dataframe
        goods_df = prepare_goods_dataframe(company["goods"])
        
        # Filter goods by search term if provided
        if search_goods:
            goods_df = goods_df[goods_df['Produced Goods'].str.contains(search_goods, case=False, na=False)]
        
        # Update live prices
        goods_df = update_live_prices(goods_df, price_data)
        
        # Calculate Guildees Pay
        goods_df = calculate_all_guildees_prices(goods_df)
        
        # Reset index to ensure it's a range index for data editor
        goods_df = goods_df.reset_index(drop=True)
        
        # Render data editor
        edited_goods = st.data_editor(
            goods_df,
            hide_index=True,
            width="stretch",
            num_rows="dynamic",
            key=f"table_{company['name']}_{idx}",
            disabled=["Guildees Pay:", "Live EXC Price", "Live AVG Price"],
            column_config=get_column_config(materials, st.session_state.planets)
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
            save_google_sheets_data(st.session_state.companies)
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
    
    # Normal UI flow - load CSS
    load_custom_css()
    
    # Title
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.markdown(APP_SUBTITLE)
    
    # Add API info banner
    with st.expander("🔌 REST API Access Available", expanded=False):
        # Check if API is available
        try:
            from streamlit.starlette import App as StarletteApp
            api_available = True
            api_status = "✅ API endpoints are active"
        except ImportError:
            api_available = False
            api_status = f"⚠️ API not available (Streamlit {st.__version__} - requires 1.53+)"
        
        st.caption(api_status)
        st.markdown("""
        Access guild data programmatically via REST API endpoints:
        
        **Available Endpoints:**
        - `GET /api/health` - Health check
        - `GET /api/goods` - List all goods
        - `GET /api/companies` - List all companies
        - `GET /api/good/{name}` - Get pricing for a specific good
        - `GET /api/company/{name}` - Get company details
        - `GET /api/all` - Get complete dataset
        
        **Example:**
        ```bash
        curl http://localhost:8503/api/good/Steel
        ```
        
        See API.md file in the project root for full documentation.
        """)
    
    # Refresh from Google Sheets if needed
    refresh_from_google_sheets()
    
    # Update local times (in case time has changed)
    if st.session_state.companies:
        st.session_state.companies = update_company_local_times(st.session_state.companies)
    
    # Fetch live prices (cached for 10 minutes)
    price_data, last_update = fetch_material_prices()
    
    # Collect all professions from companies
    all_professions = set(PROFESSIONS)  # Start with the base list
    for company in companies:
        for prof in company.get('professions', []):
            if prof and prof.strip():  # Only add non-empty professions
                all_professions.add(prof.strip())
    professions_list = sorted(list(all_professions))
    
    # Filter professions to ensure all defaults are in options
    # Clean up company professions to match available options
    for company in companies:
        valid_profs = [p for p in company.get('professions', []) if p in professions_list]
        company['professions'] = valid_profs
    
    # Render sidebar and get filter values
    selected_professions, search_company, search_goods = render_sidebar_filters(
        professions_list, price_data, last_update, st.session_state.last_sheet_refresh
    )
    
    # Automatically update API data with current prices
    if price_data and st.session_state.companies:
        # Check if we need to update API data (track last update time)
        if 'last_api_data_update' not in st.session_state:
            st.session_state.last_api_data_update = None
        
        # Update if we haven't updated yet, or if prices were just refreshed
        from datetime import datetime, timezone, timedelta
        now = datetime.now(timezone.utc)
        should_update = (
            st.session_state.last_api_data_update is None or
            (now - st.session_state.last_api_data_update) > timedelta(minutes=10)
        )
        
        if should_update:
            # Update all companies with current prices
            companies_copy = []
            for company in st.session_state.companies:
                company_copy = company.copy()
                goods_df = prepare_goods_dataframe(company["goods"])
                goods_df = update_live_prices(goods_df, price_data)
                goods_df = calculate_all_guildees_prices(goods_df)
                company_copy["goods"] = goods_df.to_dict('records')
                companies_copy.append(company_copy)
            
            # Save to API data file (not the main file to avoid affecting UI)
            save_google_sheets_data(companies_copy)
            st.session_state.last_api_data_update = now
    
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
        render_company_editor(company, idx, materials, price_data, professions_list, search_goods)
    
    # Footer
    st.info("💾 All changes are saved automatically")
    st.divider()
    st.write(f"**Showing {len(filtered_companies)} of {len(companies)} companies**")


# ============================================================================
# Streamlit App with Starlette API Routes
# ============================================================================

# Create the Streamlit app with API routes
# This must be at module level for Streamlit Cloud to recognize it
try:
    from streamlit.starlette import App
    from starlette.routing import Route
    
    app = App(
        __file__,
        routes=[
            Route("/api/health", api_health),
            Route("/api/goods", api_goods_list),
            Route("/api/companies", api_companies_list),
            Route("/api/good/{good_name}", api_good_detail),
            Route("/api/company/{company_name}", api_company_detail),
            Route("/api/all", api_all_data),
        ],
    )
    print(f"✅ Starlette API routes registered successfully")
except ImportError as e:
    # Streamlit version doesn't support Starlette integration
    print(f"⚠️ Streamlit Starlette not available: {e}")
    print(f"⚠️ Streamlit version: {st.__version__}")
    app = None
except Exception as e:
    print(f"❌ Error creating Starlette app: {e}")
    app = None


if __name__ == "__main__":
    main()
