"""Export data to public JSON file for GitHub raw content access."""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


def export_to_public_json(companies: List[Dict[str, Any]], export_dir: str = "api_exports"):
    """Export comprehensive goods data to a single JSON file with cheapest prices and all listings."""
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
    
    # Export single comprehensive file
    with open(export_path / "all_goods.json", "w") as f:
        json.dump({
            "status": "success",
            "last_updated": datetime.now().isoformat(),
            "goods_count": len(all_goods_output),
            "data": all_goods_output
        }, f, indent=2)
    
    print(f"✅ Exported {len(all_goods_output)} goods to {export_path / 'all_goods.json'}")
