"""Main application file for TiT Guild App."""
import streamlit as st
import warnings
import hashlib
import json

# Suppress FutureWarning from Streamlit's data_editor
warnings.filterwarnings('ignore', category=FutureWarning, module='streamlit.elements.widgets.data_editor')

# Import local modules
from config import APP_TITLE, APP_ICON, APP_SUBTITLE, CSS_FILE, PROFESSIONS, TIMEZONE_OPTIONS
from core.data_manager import (
    load_game_materials, load_game_planets, load_data, save_data, 
    prepare_goods_dataframe
)
from integrations.api_client import fetch_material_prices
from business.price_calculator import update_live_prices, calculate_all_guildees_prices
from core.validators import validate_goods
from business.stats import calculate_unique_goods, calculate_average_discount, get_unique_professions
from business.filters import apply_all_filters
from ui.ui_components import render_sidebar_filters, render_stats_row, get_column_config
from integrations.timezone_utils import update_company_local_times, get_local_time
from integrations.google_sheets import import_from_google_sheet
from datetime import datetime, timedelta, timezone


# ============================================================================
# Streamlit UI Functions
# ============================================================================

def get_data_version(companies):
    """Generate a version hash from companies data to detect changes."""
    data_str = json.dumps(companies, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()[:8]


def export_json_if_needed():
    """Export JSON with current prices after any data change (without pushing)."""
    try:
        from integrations.api_client import fetch_material_prices
        from integrations.json_exporter import export_to_public_json
        
        price_data, _ = fetch_material_prices()
        
        if price_data and st.session_state.companies:
            # Update all companies with current prices
            companies_copy = []
            for company in st.session_state.companies:
                company_copy = company.copy()
                goods_df = prepare_goods_dataframe(company["goods"])
                goods_df = update_live_prices(goods_df, price_data)
                goods_df = calculate_all_guildees_prices(goods_df)
                company_copy["goods"] = goods_df.to_dict('records')
                companies_copy.append(company_copy)
            
            # Export to public JSON
            export_to_public_json(companies_copy)
            print("✅ Exported JSON after data change")
    except Exception as e:
        print(f"Error exporting JSON: {e}")


def push_to_github_now(force=False):
    """Push JSON to GitHub if 2 minutes have passed or if forced. Returns (success, message)."""
    from pathlib import Path
    from integrations.github_uploader import push_to_github
    import subprocess
    
    now = datetime.now(timezone.utc)
    
    # Check if we should push (2 minutes = 120 seconds)
    if not force:
        if 'last_github_push' in st.session_state and st.session_state.last_github_push:
            time_since_push = (now - st.session_state.last_github_push).total_seconds()
            if time_since_push < 120:
                print(f"⏱️ Skipping push, only {int(time_since_push)}s since last push")
                return False, f"Skipped (last push {int(time_since_push)}s ago)"
    
    try:
        # Try GitHub API first (works remotely with token in secrets)
        repo_root = Path(__file__).parent.parent
        all_goods_path = repo_root / "api_exports" / "all_goods.json"
        all_companies_path = repo_root / "api_exports" / "all_companies.json"
        
        # Push both files via GitHub API
        success_goods = push_to_github(
            file_path=str(all_goods_path),
            repo_owner="VincentvanderLinden",
            repo_name="gt_guild_app",
            commit_message=f"Auto-update guild data - {now.strftime('%Y-%m-%d %H:%M')}"
        )
        
        success_companies = push_to_github(
            file_path=str(all_companies_path),
            repo_owner="VincentvanderLinden",
            repo_name="gt_guild_app",
            commit_message=f"Auto-update guild data - {now.strftime('%Y-%m-%d %H:%M')}"
        )
        
        success = success_goods and success_companies
        
        # Fallback to git command (works locally)
        if not success:
            try:
                # Add both JSON files
                subprocess.run(
                    ["git", "add", "api_exports/all_goods.json", "api_exports/all_companies.json"],
                    cwd=repo_root,
                    capture_output=True,
                    timeout=5
                )
                
                # Commit them
                result = subprocess.run(
                    ["git", "commit", "-m", f"Auto-update guild data - {now.strftime('%Y-%m-%d %H:%M')}"],
                    cwd=repo_root,
                    capture_output=True,
                    timeout=5
                )
                
                # Check if commit succeeded or there was nothing to commit
                if result.returncode == 0:
                    # New commit created, try to push
                    push_result = subprocess.run(
                        ["git", "push"],
                        cwd=repo_root,
                        capture_output=True,
                        timeout=10
                    )
                    if push_result.returncode == 0:
                        success = True
                        print("✅ Pushed to GitHub via git")
                    else:
                        error_msg = push_result.stderr.decode() if push_result.stderr else push_result.stdout.decode()
                        print(f"❌ Git push failed: {error_msg}")
                        # Try to recover by fetching and retrying
                        if b"rejected" in push_result.stderr or b"fetch first" in push_result.stderr:
                            print("Attempting to fetch and merge...")
                            subprocess.run(["git", "fetch"], cwd=repo_root, capture_output=True, timeout=10)
                            subprocess.run(["git", "merge", "origin/main", "--no-edit"], cwd=repo_root, capture_output=True, timeout=10)
                            retry_push = subprocess.run(["git", "push"], cwd=repo_root, capture_output=True, timeout=10)
                            if retry_push.returncode == 0:
                                success = True
                                print("✅ Pushed to GitHub after merge")
                            else:
                                return False, "Push rejected after merge attempt"
                        else:
                            return False, f"Git push failed: {error_msg[:100]}"
                elif result.returncode == 1 and b"nothing to commit" in result.stdout:
                    # No changes, but try to push any unpushed commits
                    push_result = subprocess.run(
                        ["git", "push"],
                        cwd=repo_root,
                        capture_output=True,
                        timeout=10
                    )
                    if push_result.returncode == 0:
                        success = True
                        print("✅ Pushed existing commits to GitHub")
                    else:
                        print("No new changes to push")
                        return False, "No new changes to push"
                else:
                    error_msg = result.stderr.decode() if result.stderr else "Unknown error"
                    print(f"❌ Git commit failed: {error_msg}")
                    return False, f"Git commit failed: {error_msg[:100]}"
                    
            except Exception as git_error:
                print(f"Note: Could not auto-push to GitHub: {git_error}")
                return False, f"Exception: {str(git_error)[:100]}"
        
        if success:
            st.session_state.last_github_push = now
            return True, "Successfully pushed to GitHub"
    except Exception as e:
        print(f"Error pushing to GitHub: {e}")
        return False, f"Error: {str(e)[:100]}"


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
    
    if 'last_github_push' not in st.session_state:
        st.session_state.last_github_push = None
    
    if 'sheet_url' not in st.session_state:
        # Read Google Sheet URL from secrets
        try:
            st.session_state.sheet_url = st.secrets.get("GOOGLE_SHEET_URL", "")
        except:
            st.session_state.sheet_url = ""
    
    if 'data_version' not in st.session_state:
        st.session_state.data_version = None


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
                
                # Save to main data file
                save_data(companies)
                
                # Update session state
                st.session_state.companies = companies
                st.session_state.last_sheet_refresh = now
                st.session_state.data_version = get_data_version(companies)
                
                # Export to JSON whenever we refresh from Google Sheets
                try:
                    # Get current price data
                    from integrations.api_client import fetch_material_prices
                    from integrations.json_exporter import export_to_public_json
                    price_data, _ = fetch_material_prices()
                    
                    if price_data:
                        # Update all companies with current prices
                        companies_copy = []
                        for company in companies:
                            company_copy = company.copy()
                            goods_df = prepare_goods_dataframe(company["goods"])
                            goods_df = update_live_prices(goods_df, price_data)
                            goods_df = calculate_all_guildees_prices(goods_df)
                            company_copy["goods"] = goods_df.to_dict('records')
                            companies_copy.append(company_copy)
                        
                        # Export to public JSON (push will happen via auto-push every 2 mins)
                        export_to_public_json(companies_copy)
                except Exception as e:
                    print(f"Error exporting JSON: {e}")
                
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
                        export_json_if_needed()
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
                        export_json_if_needed()
                        break
        
        # Prepare goods dataframe
        goods_df = prepare_goods_dataframe(company["goods"])
        
        # Filter out empty rows from existing data
        goods_df = goods_df[
            goods_df['Produced Goods'].notna() & 
            (goods_df['Produced Goods'].str.strip() != '') &
            (goods_df['Produced Goods'].str.strip() != 'nan')
        ].reset_index(drop=True)
        
        # Filter goods by search term if provided
        if search_goods:
            goods_df = goods_df[goods_df['Produced Goods'].str.contains(search_goods, case=False, na=False)]
        
        # Update live prices
        goods_df = update_live_prices(goods_df, price_data)
        
        # Calculate Guildees Pay
        goods_df = calculate_all_guildees_prices(goods_df)
        
        # Reset index to ensure it's a range index for data editor
        goods_df = goods_df.reset_index(drop=True)
        
        # Calculate height based on number of rows (35px per row + 38px header + 35px for empty row)
        table_height = min(35 * len(goods_df) + 73, 800)
        
        # Render data editor
        edited_goods = st.data_editor(
            goods_df,
            hide_index=True,
            width="stretch",
            height=table_height,
            num_rows="dynamic",
            key=f"table_{company['name']}_{idx}",
            disabled=["Guildees Pay:", "Live EXC Price", "Live AVG Price"],
            column_config=get_column_config(materials, st.session_state.planets)
        )
        
        # Handle changes
        if not goods_df.equals(edited_goods):
            handle_goods_changes(company, edited_goods, price_data)


@st.fragment(run_every=5)  # Refresh every 5 seconds
def render_companies_fragment(filtered_companies, materials, price_data, professions_list, search_goods):
    """Auto-refreshing fragment that renders company editors and checks for changes."""
    # Reload data to check for changes
    from core.data_manager import load_data
    latest_companies = load_data()
    
    if latest_companies:
        latest_version = get_data_version(latest_companies)
        
        # Check if data was modified by another user
        if st.session_state.data_version and latest_version != st.session_state.data_version:
            st.warning("⚠️ Data was updated by another user or process. Showing latest version.")
            st.session_state.companies = latest_companies
            st.session_state.data_version = latest_version
            
            # Update filtered companies with latest data
            from business.filters import apply_all_filters
            # Re-apply filters to get fresh filtered list - read from widget session state
            filtered_companies = apply_all_filters(
                latest_companies,
                st.session_state.get('professions_filter', []),
                st.session_state.get('search_company', ''),
                st.session_state.get('search_goods', '')
            )
    
    # Render company editors
    for idx, company in enumerate(filtered_companies):
        render_company_editor(company, idx, materials, price_data, professions_list, search_goods)


def handle_goods_changes(company, edited_goods, price_data):
    """Handle changes to company goods data."""
    # Filter out rows with empty "Produced Goods"
    edited_goods = edited_goods[
        edited_goods['Produced Goods'].notna() & 
        (edited_goods['Produced Goods'].str.strip() != '') &
        (edited_goods['Produced Goods'].str.strip() != 'nan')
    ].copy()
    
    # If all rows were removed, keep empty list
    if len(edited_goods) == 0:
        for c in st.session_state.companies:
            if c["name"] == company["name"]:
                c["goods"] = []
                save_data(st.session_state.companies)
                st.session_state.data_version = get_data_version(st.session_state.companies)
                export_json_if_needed()
                st.rerun()
                break
        return
    
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
            st.session_state.data_version = get_data_version(st.session_state.companies)
            export_json_if_needed()
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
    
    # Add JSON data access info
    with st.expander("📊 Public Data Access", expanded=False):
        st.info("""
        **JSON Data Available via GitHub:**
        
        Guild data is exported to public JSON files that update automatically:
        
        **By Good (find cheapest prices):**
        ```
        https://raw.githubusercontent.com/VincentvanderLinden/gt_guild_app/main/api_exports/all_goods.json
        ```
        
        **By Company (see all offers per company):**
        ```
        https://raw.githubusercontent.com/VincentvanderLinden/gt_guild_app/main/api_exports/all_companies.json
        ```
        
        **Data Structure:**
        - `all_goods.json`: Each good includes cheapest price, company, planet, and all listings sorted by price
        - `all_companies.json`: Each company includes professions, timezone, and all their goods with prices
        
        **JavaScript Example:**
        ```javascript
        // Get all goods
        fetch('https://raw.githubusercontent.com/VincentvanderLinden/gt_guild_app/main/api_exports/all_goods.json')
            .then(r => r.json())
            .then(data => console.log(data.data));
        
        // Get all companies
        fetch('https://raw.githubusercontent.com/VincentvanderLinden/gt_guild_app/main/api_exports/all_companies.json')
            .then(r => r.json())
            .then(data => console.log(data.data));
        ```
        
        **Python Example:**
        ```python
        import requests
        
        # Get all goods
        goods_url = "https://raw.githubusercontent.com/VincentvanderLinden/gt_guild_app/main/api_exports/all_goods.json"
        goods = requests.get(goods_url).json()["data"]
        
        # Get all companies
        companies_url = "https://raw.githubusercontent.com/VincentvanderLinden/gt_guild_app/main/api_exports/all_companies.json"
        companies = requests.get(companies_url).json()["data"]
        ```
        
        Data updates automatically every 10 minutes when prices refresh.
        """)
    
    # Refresh from Google Sheets if needed
    refresh_from_google_sheets()
    
    # Update local times (in case time has changed)
    if st.session_state.companies:
        st.session_state.companies = update_company_local_times(st.session_state.companies)
    
    # Force refresh on first app load (once per session)
    if 'initial_refresh_done' not in st.session_state:
        st.session_state.initial_refresh_done = False
    
    if not st.session_state.initial_refresh_done:
        with st.spinner("Loading guild data from Google Sheets..."):
            # Force Google Sheets refresh on startup
            st.session_state.last_sheet_refresh = None
            refresh_from_google_sheets()
        st.session_state.initial_refresh_done = True
    
    # Push to GitHub on app startup (once per session)
    if 'initial_push_done' not in st.session_state:
        st.session_state.initial_push_done = False
    
    if not st.session_state.initial_push_done:
        result = push_to_github_now(force=True)
        # Result might be bool or tuple, handle both
        if not isinstance(result, bool):
            success, _ = result
        st.session_state.initial_push_done = True
    
    # Fetch live prices (cached for 10 minutes, but will be fresh on startup)
    with st.spinner("Fetching live market prices..."):
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
    selected_professions, search_company, search_goods, push_button = render_sidebar_filters(
        professions_list, price_data, last_update, st.session_state.last_sheet_refresh, 
        st.session_state.last_github_push
    )
    
    # Handle manual push button
    if push_button:
        with st.spinner("Pushing to GitHub..."):
            success, message = push_to_github_now(force=True)
            if success:
                st.success(f"✅ {message}")
                st.info("Note: GitHub raw CDN may take 1-2 minutes to update")
            else:
                st.error(f"❌ {message}")
    
    # Auto-push every 2 minutes
    result = push_to_github_now(force=False)
    # Result might be bool (old code) or tuple (new code), handle both
    if not isinstance(result, bool):
        success, _ = result
        # If auto-push succeeded, refresh to update sidebar times
        if success:
            st.rerun()
    
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
    
    # Store current data version before rendering
    if st.session_state.data_version is None:
        st.session_state.data_version = get_data_version(st.session_state.companies)
    
    # Render companies with auto-refresh fragment
    render_companies_fragment(filtered_companies, materials, price_data, professions_list, search_goods)
    
    # Footer
    st.info("💾 All changes are saved automatically")
    st.divider()
    st.write(f"**Showing {len(filtered_companies)} of {len(companies)} companies**")


if __name__ == "__main__":
    main()
