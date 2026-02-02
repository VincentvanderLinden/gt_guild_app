"""API client for Galactic Tycoons exchange data"""
import requests
from typing import Dict, Optional, Tuple
from datetime import datetime, timezone
import streamlit as st


@st.cache_data(ttl=600)  # Cache for 10 minutes (600 seconds)
def fetch_material_prices() -> Tuple[Dict[str, Dict[str, float]], str]:
    """
    Fetch material prices from the Galactic Tycoons API.
    Returns a tuple of (price_dict, timestamp_utc).
    Cached for 10 minutes.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    try:
        response = requests.get(
            "https://api.g2.galactictycoons.com/public/exchange/mat-prices",
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Convert to dictionary keyed by material name for easy lookup
        # API returns prices in cents, convert to dollars
        price_dict = {}
        for item in data.get("prices", []):
            material_name = item.get("matName")
            if material_name:
                price_dict[material_name] = {
                    "id": item.get("matId"),
                    "currentPrice": item.get("currentPrice", 0) / 100,
                    "avgPrice": item.get("avgPrice", 0) / 100
                }
        
        return price_dict, timestamp
    
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not fetch live prices: {e}")
        return {}, timestamp
    except Exception as e:
        st.error(f"Error processing price data: {e}")
        return {}, timestamp


def get_material_price(material_name: str, price_dict: Optional[Dict] = None) -> Dict[str, float]:
    """
    Get price information for a specific material.
    Returns dict with currentPrice and avgPrice, or zeros if not found.
    """
    if price_dict is None:
        price_dict = fetch_material_prices()
    
    return price_dict.get(material_name, {
        "id": None,
        "currentPrice": 0,
        "avgPrice": 0
    })
