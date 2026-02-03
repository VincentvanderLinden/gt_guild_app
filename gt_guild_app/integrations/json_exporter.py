"""Export data to public JSON file for GitHub raw content access."""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


def export_to_public_json(companies: List[Dict[str, Any]], export_dir: str = "api_exports"):
    """Export comprehensive data to JSON files: all_goods.json and all_companies.json."""
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    
    # Build comprehensive goods data with all listings sorted by price
    goods_data = {}
    for company in companies:
        for good in company['goods']:
            good_name = good.get('Produced Goods', '')
            if not good_name:
                continue
            
            if good_name not in goods_data:
                goods_data[good_name] = []
            
            goods_data[good_name].append({
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
    
    # Sort each good's listings by cheapest price and format output
    all_goods_output = []
    for good_name in sorted(goods_data.keys()):
        listings = goods_data[good_name]
        listings.sort(key=lambda x: x['guildees_pay'])
        
        all_goods_output.append({
            'good': good_name,
            'cheapest_price': listings[0]['guildees_pay'] if listings else 0,
            'cheapest_company': listings[0]['company'] if listings else None,
            'cheapest_planet': listings[0]['planet_produced'] if listings else None,
            'listings_count': len(listings),
            'listings': listings
        })
    
    # Export all_goods.json (organized by goods)
    with open(export_path / "all_goods.json", "w") as f:
        json.dump({
            "status": "success",
            "last_updated": datetime.now().isoformat(),
            "goods_count": len(all_goods_output),
            "data": all_goods_output
        }, f, indent=2)
    
    print(f"✅ Exported {len(all_goods_output)} goods to {export_path / 'all_goods.json'}")
    
    # Build all_companies.json (organized by companies)
    all_companies_output = []
    for company in companies:
        if not company.get('goods'):
            continue
        
        # Sort company's goods by name
        company_goods = sorted(company['goods'], key=lambda x: x.get('Produced Goods', ''))
        
        all_companies_output.append({
            'company': {
                'name': company['name'],
                'industry': company.get('industry', ''),
                'professions': company.get('professions', []),
                'timezone': company.get('timezone', 'UTC +00:00'),
                'local_time': company.get('local_time', 'N/A'),
                'goods_count': len(company_goods),
                'goods': [{
                    'good': good.get('Produced Goods', ''),
                    'planet_produced': good.get('Planet Produced', ''),
                    'guildees_pay': good.get('Guildees Pay:', 0),
                    'live_exc_price': good.get('Live EXC Price', 0),
                    'live_avg_price': good.get('Live AVG Price', 0),
                    'guild_max': good.get('Guild Max', 0),
                    'guild_min': good.get('Guild Min', 0),
                    'discount_percent': good.get('Guild % Discount', 0),
                    'discount_fixed': good.get('Guild Fixed Discount', 0)
                } for good in company_goods]
            }
        })
    
    # Sort companies by name
    all_companies_output.sort(key=lambda x: x['company']['name'])
    
    # Export all_companies.json (organized by companies)
    with open(export_path / "all_companies.json", "w") as f:
        json.dump({
            "status": "success",
            "last_updated": datetime.now().isoformat(),
            "companies_count": len(all_companies_output),
            "data": all_companies_output
        }, f, indent=2)
    
    print(f"✅ Exported {len(all_companies_output)} companies to {export_path / 'all_companies.json'}")
