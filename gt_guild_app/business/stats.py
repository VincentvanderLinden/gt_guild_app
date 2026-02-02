"""Statistics calculation utilities."""
import pandas as pd
from typing import List, Dict, Any, Set


def calculate_unique_goods(companies: List[Dict[str, Any]]) -> int:
    """Calculate the number of unique goods being sold."""
    unique_goods = set()
    for c in companies:
        for g in c["goods"]:
            good_name = g.get("Produced Goods", "")
            if good_name:  # Exclude empty strings
                unique_goods.add(good_name)
    return len(unique_goods)


def calculate_average_discount(companies: List[Dict[str, Any]]) -> float:
    """Calculate average discount percentage across all companies."""
    all_discounts = [
        g.get("Guild % Discount", 0) 
        for c in companies 
        for g in c["goods"] 
        if g.get("Guild % Discount") is not None and not pd.isna(g.get("Guild % Discount"))
    ]
    
    if all_discounts and len(all_discounts) > 0:
        return sum(all_discounts) / len(all_discounts)
    return 0.0


def get_unique_professions(companies: List[Dict[str, Any]]) -> Set[str]:
    """Get set of all unique professions used across companies."""
    all_professions = set()
    for c in companies:
        all_professions.update(c.get('professions', []))
    return all_professions
