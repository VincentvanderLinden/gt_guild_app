"""Price calculation and rounding logic."""
import math
import pandas as pd
from typing import Dict, Any


def calculate_guildees_pay(live_price: float, discount_percent: float) -> float:
    """
    Calculate guildees pay from live price and discount percentage.
    Applies smart rounding based on price ranges.
    """
    # Apply discount
    price = live_price * (1 - discount_percent / 100)
    
    # Apply tiered rounding rules
    if price < 50:
        return math.ceil(price * 2) / 2  # Round to nearest 0.5
    elif price < 100:
        return math.ceil(price)  # Round to nearest 1
    elif price < 1000:
        return math.ceil(price / 10) * 10  # Round to nearest 10
    elif price < 5000:
        return math.ceil(price / 50) * 50  # Round to nearest 50
    elif price < 10000:
        return math.ceil(price / 100) * 100  # Round to nearest 100
    elif price < 50000:
        return math.ceil(price / 500) * 500  # Round to nearest 500
    elif price < 100000:
        return math.ceil(price / 1000) * 1000  # Round to nearest 1000
    else:
        return math.ceil(price / 1000) * 1000  # Round to nearest 1000


def apply_price_bounds(price: float, guild_min: float, guild_max: float) -> float:
    """Apply guild min/max bounds to calculated price."""
    if guild_min > 0 and price < guild_min:
        return guild_min
    elif guild_max > 0 and price > guild_max:
        return guild_max
    return price


def update_live_prices(goods_df: pd.DataFrame, price_data: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """Update DataFrame with live prices from API."""
    if not price_data:
        return goods_df
    
    for idx, row in goods_df.iterrows():
        material_name = row.get('Produced Goods', '')
        if material_name in price_data:
            goods_df.at[idx, 'Live EXC Price'] = int(price_data[material_name]['currentPrice'])
            goods_df.at[idx, 'Live AVG Price'] = int(price_data[material_name]['avgPrice'])
    
    return goods_df


def calculate_all_guildees_prices(goods_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate Guildees Pay for all goods based on live prices and discounts."""
    for idx, row in goods_df.iterrows():
        live_price = row.get('Live EXC Price', 0)
        discount = row.get('Guild % Discount', 0)
        guild_min = row.get('Guild Min', 0)
        guild_max = row.get('Guild Max', 0)
        
        # Calculate base price with discount and rounding
        calculated_price = calculate_guildees_pay(live_price, discount)
        
        # Apply bounds
        final_price = apply_price_bounds(calculated_price, guild_min, guild_max)
        
        goods_df.at[idx, 'Guildees Pay:'] = final_price
    
    return goods_df
