"""Data loading, saving, and transformation utilities."""
import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from config import DATA_FILE, GAMEDATA_FILE


def load_game_materials() -> List[str]:
    """Load materials from game data file."""
    try:
        with open(GAMEDATA_FILE) as f:
            gamedata = json.load(f)
            materials = [material['name'] for material in gamedata.get('materials', [])]
            return sorted(materials)
    except Exception as e:
        return []


def feather_to_companies(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert flattened feather DataFrame to nested company structure."""
    companies = []
    for company_name in df['company_name'].unique():
        company_df = df[df['company_name'] == company_name].iloc[0]
        goods_df = df[df['company_name'] == company_name][[
            'Produced Goods', 'Guildees Pay:', 'Live EXC Price', 'Live AVG Price',
            'Guild Max', 'Guild Min', 'Guild % Discount', 'Guild Fixed Discount'
        ]]
        
        # Parse professions from comma-separated string
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


def companies_to_feather(companies: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert nested company structure to flattened DataFrame for feather format."""
    # Define expected columns to ensure consistency
    expected_columns = [
        'company_name', 'industry', 'professions', 'timezone', 'local_time',
        'Produced Goods', 'Guildees Pay:', 'Live EXC Price', 'Live AVG Price',
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
                'timezone': company['timezone'],
                'local_time': company['local_time'],
                'Produced Goods': good.get('Produced Goods', ''),
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


def prepare_goods_dataframe(goods: List[Dict[str, Any]]) -> pd.DataFrame:
    """Prepare goods DataFrame with proper data types."""
    goods_df = pd.DataFrame(goods)
    
    # Integer columns
    numeric_int_columns = ['Live EXC Price', 'Live AVG Price', 
                           'Guild Max', 'Guild Min', 'Guild % Discount', 'Guild Fixed Discount']
    for col in numeric_int_columns:
        if col in goods_df.columns:
            goods_df[col] = pd.to_numeric(goods_df[col], errors='coerce').fillna(0).astype(int)
    
    # Float column (supports decimal rounding like 34.5)
    if 'Guildees Pay:' in goods_df.columns:
        goods_df['Guildees Pay:'] = pd.to_numeric(goods_df['Guildees Pay:'], errors='coerce').fillna(0).astype(float)
    
    return goods_df
