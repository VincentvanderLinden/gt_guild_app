"""Data filtering utilities."""
from typing import List, Dict, Any


def filter_by_professions(companies: List[Dict[str, Any]], professions: List[str]) -> List[Dict[str, Any]]:
    """Filter companies by selected professions."""
    if not professions:
        return companies
    return [c for c in companies if any(p in c.get('professions', []) for p in professions)]


def filter_by_company_name(companies: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
    """Filter companies by name search."""
    if not search_term:
        return companies
    return [c for c in companies if search_term.lower() in c["name"].lower()]


def filter_by_goods_name(companies: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
    """Filter companies that have goods matching the search term."""
    if not search_term:
        return companies
    return [
        c for c in companies 
        if any(search_term.lower() in g["Produced Goods"].lower() for g in c["goods"])
    ]


def apply_all_filters(companies: List[Dict[str, Any]], 
                     professions: List[str],
                     company_search: str,
                     goods_search: str) -> List[Dict[str, Any]]:
    """Apply all filters in sequence."""
    filtered = companies.copy()
    filtered = filter_by_professions(filtered, professions)
    filtered = filter_by_company_name(filtered, company_search)
    filtered = filter_by_goods_name(filtered, goods_search)
    return filtered
