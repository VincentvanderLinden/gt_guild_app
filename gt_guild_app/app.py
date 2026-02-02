import streamlit as st
import pandas as pd
import json
from pathlib import Path
from api_client import fetch_material_prices

# Page configuration
st.set_page_config(
    page_title="TiT Guild App™",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and apply custom CSS
CSS_FILE = Path(__file__).parent / "assets" / "css" / "style.css"
with open(CSS_FILE) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Data persistence
DATA_FILE = Path(__file__).parent / "assets" / "data" / "guild_data.feather"
DEFAULT_DATA_FILE = Path(__file__).parent / "assets" / "data" / "default_guild_data.feather"
GAMEDATA_FILE = Path(__file__).parent / "assets" / "data" / "gamedata.json"

# Available professions (sorted alphabetically)
PROFESSIONS = sorted([
    "Construction",
    "Manufacturing",
    "Agriculture",
    "Resource Extraction",
    "Metallurgy",
    "Chemistry",
    "Electronics",
    "Food Production",
    "Science",
    "Chicken Farmer",
    "ConstRICtion",
    "Transporting",
    "Jack-of-all-Trades",
    "Failing Hard"
])


def load_game_materials():
    """Load materials from game data file"""
    try:
        with open(GAMEDATA_FILE) as f:
            gamedata = json.load(f)
            # Extract material names from the materials list
            materials = [material['name'] for material in gamedata.get('materials', [])]
            return sorted(materials)
    except Exception as e:
        st.error(f"Error loading game data: {e}")
        return []


def load_default_data():
    """Load default data from feather file"""
    df = pd.read_feather(DEFAULT_DATA_FILE)
    # Convert to nested structure
    companies = []
    for company_name in df['company_name'].unique():
        company_df = df[df['company_name'] == company_name].iloc[0]
        goods_df = df[df['company_name'] == company_name][[
            'Produced Goods', 'Guildees Pay:', 'Live EXC Price', 'Live AVG Price',
            'Guild Max', 'Guild Min', 'Guild % Discount', 'Guild Fixed Discount'
        ]]
        # Load professions from comma-separated string, or use industry as default
        professions_str = company_df.get('professions', company_df['industry'])
        professions = [p.strip() for p in professions_str.split(',')] if professions_str else []
        
        companies.append({
            'name': company_df['company_name'],
            'industry': company_df['industry'],
            'professions': professions,
            'timezone': company_df['timezone'],
            'local_time': company_df['local_time'],
            'goods': goods_df.to_dict('records')
        })
    return companies


def load_data():
    """Load data from feather file or return default data"""
    if DATA_FILE.exists():
        try:
            df = pd.read_feather(DATA_FILE)
            # Convert back to nested structure
            companies = []
            for company_name in df['company_name'].unique():
                company_df = df[df['company_name'] == company_name].iloc[0]
                goods_df = df[df['company_name'] == company_name][[
                    'Produced Goods', 'Guildees Pay:', 'Live EXC Price', 'Live AVG Price',
                    'Guild Max', 'Guild Min', 'Guild % Discount', 'Guild Fixed Discount'
                ]]
                # Load professions from comma-separated string
                professions_str = company_df.get('professions', company_df['industry'])
                professions = [p.strip() for p in professions_str.split(',')] if professions_str else []
                
                companies.append({
                    'name': company_df['company_name'],
                    'industry': company_df['industry'],
                    'professions': professions,
                    'timezone': company_df['timezone'],
                    'local_time': company_df['local_time'],
                    'goods': goods_df.to_dict('records')
                })
            return companies
        except Exception:
            return None
    return None


def save_data(companies):
    """Save data to feather file"""
    # Flatten nested structure for feather format
    rows = []
    for company in companies:
        # Convert professions list to comma-separated string
        professions_str = ', '.join(company.get('professions', []))
        for good in company['goods']:
            rows.append({
                'company_name': company['name'],
                'industry': company['industry'],
                'professions': professions_str,
                'timezone': company['timezone'],
                'local_time': company['local_time'],
                **good
            })
    df = pd.DataFrame(rows)
    df.to_feather(DATA_FILE)


def calculate_guildees_pay(live_price, discount_percent):
    """
    Calculate guildees pay from live price and discount percentage.
    Applies smart rounding based on price ranges.
    """
    import math
    
    # Apply discount
    price = live_price * (1 - discount_percent / 100)
    
    # Apply rounding rules
    if price < 50:
        # Round to nearest 0.5
        return math.ceil(price * 2) / 2
    elif price < 100:
        # Round to nearest 1
        return math.ceil(price)
    elif price < 1000:
        # Round to nearest 10
        return math.ceil(price / 10) * 10
    elif price < 5000:
        # Round to nearest 50
        return math.ceil(price / 50) * 50
    elif price < 10000:
        # Round to nearest 100
        return math.ceil(price / 100) * 100
    elif price < 50000:
        # Round to nearest 500
        return math.ceil(price / 500) * 500
    elif price < 100000:
        # Round to nearest 1000
        return math.ceil(price / 1000) * 1000
    else:
        # Round to nearest 1000 for larger amounts
        return math.ceil(price / 1000) * 1000
    df.to_feather(DATA_FILE)


# Title
st.title("🐔 TiT Guild App™")
st.markdown("*View and manage items that players are selling*")

# Load saved data or use defaults
if 'companies' not in st.session_state:
    loaded_data = load_data()
    st.session_state.companies = loaded_data if loaded_data else load_default_data()

# Load game materials for dropdown
if 'materials' not in st.session_state:
    st.session_state.materials = load_game_materials()

# Fetch live prices (cached for 10 minutes)
price_data, last_update = fetch_material_prices()

companies = st.session_state.companies
materials = st.session_state.materials

# Sidebar filters
st.sidebar.title("⚙️ Filters")
#st.sidebar.markdown("---")
st.sidebar.space()

# Profession filter - use full professions list
selected_professions = st.sidebar.multiselect("Professions", PROFESSIONS)

search_company = st.sidebar.text_input("Search Company", "", key="search_company")

search_goods = st.sidebar.text_input("Search Goods", "", key="search_goods")

# Show price update status in sidebar
st.sidebar.divider()
if price_data:
    st.sidebar.info(f"📊 Live prices: {len(price_data)} materials\n\nLast updated: \n\n {last_update}\n\n*Updates every 10 minutes*")
else:
    st.sidebar.warning("⚠️ Could not load live prices")

# Apply filters
filtered_companies = companies.copy()

if selected_professions:
    filtered_companies = [c for c in filtered_companies if any(p in c.get('professions', []) for p in selected_professions)]

if search_company:
    filtered_companies = [c for c in filtered_companies if search_company.lower() in c["name"].lower()]

if search_goods:
    # Filter companies that have at least one good matching the search
    filtered_companies = [
        c for c in filtered_companies 
        if any(search_goods.lower() in g["Produced Goods"].lower() for g in c["goods"])
    ]

# Display stats
total_goods = sum(len(c["goods"]) for c in filtered_companies)
all_discounts = [g.get("Guild % Discount", 0) for c in filtered_companies for g in c["goods"] if g.get("Guild % Discount") is not None and not pd.isna(g.get("Guild % Discount"))]
avg_discount = sum(all_discounts) / len(all_discounts) if all_discounts and len(all_discounts) > 0 else 0

# Count unique professions
all_professions_used = set()
for c in filtered_companies:
    all_professions_used.update(c.get('professions', []))

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Companies", len(filtered_companies))
with col2:
    st.metric("Total Products", total_goods)
with col3:
    st.metric("Professions", len(all_professions_used))
with col4:
    st.metric("Avg Discount %", f"{avg_discount:.1f}%")

st.divider()

# Display each company with its own table
for idx, company in enumerate(filtered_companies):
    # Format professions display
    prof_display = ', '.join(company.get('professions', [])) if company.get('professions') else company['industry']
    with st.expander(f"**{company['name']}** - {prof_display} | {company['timezone']} ({company['local_time']})", expanded=True):
        # Allow editing professions
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
        
        # Create dataframe for this company's goods
        goods_df = pd.DataFrame(company["goods"])
        
        # Ensure all numeric columns are properly typed and convert to integers
        numeric_columns = ['Guildees Pay:', 'Live EXC Price', 'Live AVG Price', 
                          'Guild Max', 'Guild Min', 'Guild % Discount', 'Guild Fixed Discount']
        for col in numeric_columns:
            if col in goods_df.columns:
                goods_df[col] = pd.to_numeric(goods_df[col], errors='coerce').fillna(0).astype(int)
        
        # Update live prices from API
        if price_data:
            for idx, row in goods_df.iterrows():
                material_name = row.get('Produced Goods', '')
                if material_name in price_data:
                    goods_df.at[idx, 'Live EXC Price'] = int(price_data[material_name]['currentPrice'])
                    goods_df.at[idx, 'Live AVG Price'] = int(price_data[material_name]['avgPrice'])
        
        # Calculate Guildees Pay based on Live EXC Price and discount
        for idx, row in goods_df.iterrows():
            live_price = row.get('Live EXC Price', 0)
            discount = row.get('Guild % Discount', 0)
            guild_min = row.get('Guild Min', 0)
            guild_max = row.get('Guild Max', 0)
            
            # Calculate base price with discount and rounding
            calculated_price = calculate_guildees_pay(live_price, discount)
            
            # Apply bounds: if below min, use min; if above max, use max
            if guild_min > 0 and calculated_price < guild_min:
                calculated_price = guild_min
            elif guild_max > 0 and calculated_price > guild_max:
                calculated_price = guild_max
            
            goods_df.at[idx, 'Guildees Pay:'] = calculated_price
        
        # Add a special wrapper to the column name for CSS targeting
        goods_df_display = goods_df.copy()
        
        # Editable table for each company
        edited_goods = st.data_editor(
            goods_df_display,
            hide_index=True,
            width="stretch",
            num_rows="dynamic",
            key=f"table_{company['name']}_{idx}",
            disabled=["Guildees Pay:", "Live EXC Price", "Live AVG Price"],
            column_config={
                "Produced Goods": st.column_config.SelectboxColumn(
                    "Produced Goods",
                    width="medium",
                    options=materials,
                    required=True
                ),
                "Guildees Pay:": st.column_config.NumberColumn(
                    "💰 Guildees Pay 💰", 
                    format="✓ $%d",
                    help="Auto-calculated price after discount and bounds"
                ),
                "Live EXC Price": st.column_config.NumberColumn("Live EXC Price", format="$%d"),
                "Live AVG Price": st.column_config.NumberColumn("Live AVG Price", format="$%d"),
                "Guild Max": st.column_config.NumberColumn("Guild Max", format="$%d"),
                "Guild Min": st.column_config.NumberColumn("Guild Min", format="$%d"),
                "Guild % Discount": st.column_config.NumberColumn("Guild % Discount", format="%d %%"),
                "Guild Fixed Discount": st.column_config.NumberColumn("Guild Fixed Discount", format="$%d")
            }
        )
        
        # Update the company's goods in session state if changed
        if not goods_df_display.equals(edited_goods):
            # Copy changes back to original goods_df
            goods_df = edited_goods.copy()
            
            # Check for empty Produced Goods
            empty_goods = goods_df[(goods_df['Produced Goods'].isna()) | (goods_df['Produced Goods'] == '')]
            if not empty_goods.empty:
                st.error(f"⚠️ {company['name']}: All Produced Goods fields must be filled!")
            else:
                # Check for duplicate Produced Goods
                goods_list = goods_df['Produced Goods'].tolist()
                if len(goods_list) != len(set(goods_list)):
                    duplicates = [item for item in set(goods_list) if goods_list.count(item) > 1]
                    st.error(f"⚠️ {company['name']}: Duplicate goods found: {', '.join(duplicates)}")
                else:
                    # Update prices from cached data before saving
                    if price_data:
                        for idx, row in goods_df.iterrows():
                            material_name = row.get('Produced Goods', '')
                            if material_name and material_name in price_data:
                                goods_df.at[idx, 'Live EXC Price'] = int(price_data[material_name]['currentPrice'])
                                goods_df.at[idx, 'Live AVG Price'] = int(price_data[material_name]['avgPrice'])
                    
                    # Find the company in the original list and update
                    for c in st.session_state.companies:
                        if c["name"] == company["name"]:
                            c["goods"] = goods_df.to_dict('records')
                            save_data(st.session_state.companies)
                            st.rerun()  # Rerun to show updated prices immediately
                            break

# Validate all companies have filled and unique Produced Goods
def validate_all_goods():
    """Check if all Produced Goods fields are filled and unique per company"""
    for company in st.session_state.companies:
        goods_list = [good.get('Produced Goods', '') for good in company['goods']]
        
        # Check for empty
        if any(not g or g == '' for g in goods_list):
            return False, f"{company['name']} has empty Produced Goods fields"
        
        # Check for duplicates
        if len(goods_list) != len(set(goods_list)):
            duplicates = [item for item in set(goods_list) if goods_list.count(item) > 1]
            return False, f"{company['name']} has duplicate goods: {', '.join(duplicates)}"
    
    return True, None

# Show info about auto-saving
st.info("💾 All changes are saved automatically")

# Show totals
st.divider()
st.write(f"**Showing {len(filtered_companies)} of {len(companies)} companies**")
