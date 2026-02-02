"""Data validation utilities."""
from typing import List, Dict, Any, Tuple


def validate_goods(company: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate goods for a single company.
    Returns (is_valid, error_message).
    """
    goods_list = [good.get('Produced Goods', '') for good in company['goods']]
    
    # Check for empty goods
    if any(not g or g == '' for g in goods_list):
        return False, f"{company['name']}: All Produced Goods fields must be filled!"
    
    # Check for duplicates
    if len(goods_list) != len(set(goods_list)):
        duplicates = [item for item in set(goods_list) if goods_list.count(item) > 1]
        return False, f"{company['name']}: Duplicate goods found: {', '.join(duplicates)}"
    
    return True, ""


def validate_all_companies(companies: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """
    Validate all companies' goods.
    Returns (is_valid, error_message).
    """
    for company in companies:
        is_valid, error_msg = validate_goods(company)
        if not is_valid:
            return False, error_msg
    
    return True, ""
