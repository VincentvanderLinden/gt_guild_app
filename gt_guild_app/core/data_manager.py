"""Data loading, saving, and transformation utilities."""
import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DATA_FILE, GOOGLE_SHEETS_DATA_FILE, GAMEDATA_FILE, CONTRACTS_FILE, COMPANY_CONFIG_FILE


def load_game_materials() -> List[str]:
    """Load materials from game data file."""
    try:
        with open(GAMEDATA_FILE) as f:
            gamedata = json.load(f)
            materials = [material['name'] for material in gamedata.get('materials', [])]
            return sorted(materials)
    except Exception as e:
        return []


def load_game_planets() -> List[str]:
    """Load planet names from game data file."""
    try:
        with open(GAMEDATA_FILE) as f:
            gamedata = json.load(f)
            # Extract individual planet names from all systems
            planets = [planet['name'] for system in gamedata.get('systems', []) 
                      if system.get('planets') 
                      for planet in system['planets']]
            return sorted(set(planets))
    except Exception as e:
        return []


def feather_to_companies(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert flattened feather DataFrame to nested company structure."""
    companies = []
    for company_name in df['company_name'].unique():
        company_df = df[df['company_name'] == company_name].iloc[0]
        goods_df = df[df['company_name'] == company_name][[
            'Produced Goods', 'Planet Produced', 'Guildees Pay:', 'Live EXC Price', 'Live AVG Price',
            'Guild Max', 'Guild Min', 'Guild % Discount', 'Guild Fixed Discount'
        ]]
        
        # Parse professions from comma-separated string
        professions_str = company_df.get('professions', company_df['industry'])
        professions = [p.strip() for p in professions_str.split(',')] if professions_str else []
        
        companies.append({
            'name': company_df['company_name'],
            'industry': company_df['industry'],
            'professions': professions,
            'timezone': company_df.get('timezone', 'UTC +00:00'),
            'local_time': company_df.get('local_time', 'N/A'),
            'goods': goods_df.to_dict('records')
        })
    return companies


def companies_to_feather(companies: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert nested company structure to flattened DataFrame for feather format."""
    # Define expected columns to ensure consistency
    expected_columns = [
        'company_name', 'industry', 'professions', 'timezone', 'local_time',
        'Produced Goods', 'Planet Produced', 'Guildees Pay:', 'Live EXC Price', 'Live AVG Price',
        'Guild Max', 'Guild Min', 'Guild % Discount', 'Guild Fixed Discount'
    ]
    
    rows = []
    for company in companies:
        professions_str = ', '.join(company.get('professions', []))
        for good in company['goods']:
            row = {
                'company_name': company['name'],
                'industry': company['industry'],
                'professions': professions_str,
                'timezone': company.get('timezone', 'UTC +00:00'),
                'local_time': company.get('local_time', 'N/A'),
                'Produced Goods': good.get('Produced Goods', ''),
                'Planet Produced': good.get('Planet Produced', ''),
                'Guildees Pay:': good.get('Guildees Pay:', 0),
                'Live EXC Price': good.get('Live EXC Price', 0),
                'Live AVG Price': good.get('Live AVG Price', 0),
                'Guild Max': good.get('Guild Max', 0),
                'Guild Min': good.get('Guild Min', 0),
                'Guild % Discount': good.get('Guild % Discount', 0),
                'Guild Fixed Discount': good.get('Guild Fixed Discount', 0)
            }
            rows.append(row)
    
    # Create DataFrame with explicit column order
    if not rows:
        return pd.DataFrame(columns=expected_columns)
    
    return pd.DataFrame(rows, columns=expected_columns)


def load_data() -> Optional[List[Dict[str, Any]]]:
    """Load data from feather file."""
    if not DATA_FILE.exists():
        return None
    
    try:
        df = pd.read_feather(DATA_FILE)
        return feather_to_companies(df)
    except Exception:
        return None


def save_data(companies: List[Dict[str, Any]]) -> None:
    """Save company data to feather file."""
    df = companies_to_feather(companies)
    df.to_feather(DATA_FILE)


def load_google_sheets_data() -> Optional[List[Dict[str, Any]]]:
    """Load data from Google Sheets feather file for API access."""
    if not GOOGLE_SHEETS_DATA_FILE.exists():
        return None
    
    try:
        df = pd.read_feather(GOOGLE_SHEETS_DATA_FILE)
        return feather_to_companies(df)
    except Exception:
        return None


def save_google_sheets_data(companies: List[Dict[str, Any]]) -> None:
    """Save Google Sheets data to separate feather file for API access."""
    df = companies_to_feather(companies)
    GOOGLE_SHEETS_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_feather(GOOGLE_SHEETS_DATA_FILE)


def prepare_goods_dataframe(goods: List[Dict[str, Any]]) -> pd.DataFrame:
    """Prepare goods DataFrame with proper data types."""
    # Define expected dtypes to prevent FutureWarning
    dtype_spec = {
        'Produced Goods': 'str',
        'Planet Produced': 'str',
        'Guildees Pay:': 'float64',
        'Live EXC Price': 'int64',
        'Live AVG Price': 'int64',
        'Guild Max': 'int64',
        'Guild Min': 'int64',
        'Guild % Discount': 'int64',
        'Guild Fixed Discount': 'int64'
    }
    
    # Create DataFrame with explicit dtypes
    if not goods:
        # Return empty DataFrame with proper structure
        return pd.DataFrame(columns=list(dtype_spec.keys())).astype(dtype_spec)
    
    goods_df = pd.DataFrame(goods)
    
    # Integer columns
    numeric_int_columns = ['Live EXC Price', 'Live AVG Price', 
                           'Guild Max', 'Guild Min', 'Guild % Discount', 'Guild Fixed Discount']
    for col in numeric_int_columns:
        if col in goods_df.columns:
            goods_df[col] = pd.to_numeric(goods_df[col], errors='coerce').fillna(0).astype('int64')
    
    # Float column (supports decimal rounding like 34.5)
    if 'Guildees Pay:' in goods_df.columns:
        goods_df['Guildees Pay:'] = pd.to_numeric(goods_df['Guildees Pay:'], errors='coerce').fillna(0).astype('float64')
    
    # String columns
    if 'Produced Goods' in goods_df.columns:
        goods_df['Produced Goods'] = goods_df['Produced Goods'].astype('str')
    if 'Planet Produced' in goods_df.columns:
        goods_df['Planet Produced'] = goods_df['Planet Produced'].astype('str')
    
    return goods_df


def load_contracts() -> Optional[Dict[str, Any]]:
    """Load contracts data from JSON file."""
    if not CONTRACTS_FILE.exists():
        return {}
    
    try:
        # Change to JSON for nested dict structure
        import json
        contracts_json = CONTRACTS_FILE.with_suffix('.json')
        if contracts_json.exists():
            with open(contracts_json, 'r') as f:
                return json.load(f)
        return {}
    except Exception:
        return {}


def save_contracts(contracts: Dict[str, Any]) -> None:
    """Save contracts data to JSON file."""
    import json
    # Change to JSON for nested dict structure
    contracts_json = CONTRACTS_FILE.with_suffix('.json')
    with open(contracts_json, 'w') as f:
        json.dump(contracts, f, indent=2)


def load_company_config() -> Dict[str, Any]:
    """Load company configuration (enabled companies list)."""
    if not COMPANY_CONFIG_FILE.exists():
        return {'enabled_companies': []}
    
    try:
        with open(COMPANY_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {'enabled_companies': []}


def save_company_config(config: Dict[str, Any]) -> None:
    """Save company configuration to JSON file."""
    with open(COMPANY_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
