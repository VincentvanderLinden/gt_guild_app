"""Main entry point with Starlette API support."""
from streamlit.starlette import App
from starlette.routing import Route
from starlette.responses import JSONResponse
from core.data_manager import load_google_sheets_data


async def api_health(request):
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "TiT Guild App API"
    })


async def api_goods_list(request):
    """Get list of all goods across all companies."""
    companies = load_google_sheets_data()
    if not companies:
        return JSONResponse({
            "status": "error",
            "message": "No data available"
        }, status_code=404)
    
    goods_set = set()
    for company in companies:
        for good in company['goods']:
            goods_set.add(good.get('Produced Goods', ''))
    
    return JSONResponse({
        "status": "success",
        "data": {
            "goods": sorted(list(goods_set)),
            "count": len(goods_set)
        }
    })


async def api_companies_list(request):
    """Get list of all companies."""
    companies = load_google_sheets_data()
    if not companies:
        return JSONResponse({
            "status": "error",
            "message": "No data available"
        }, status_code=404)
    
    company_list = []
    for company in companies:
        company_list.append({
            "name": company['name'],
            "industry": company['industry'],
            "professions": company.get('professions', []),
            "timezone": company.get('timezone', 'UTC +00:00'),
            "goods_count": len(company['goods'])
        })
    
    return JSONResponse({
        "status": "success",
        "data": {
            "companies": company_list,
            "count": len(company_list)
        }
    })


async def api_good_detail(request):
    """Get pricing details for a specific good."""
    good_name = request.path_params.get('good_name')
    if not good_name:
        return JSONResponse({
            "status": "error",
            "message": "Good name is required"
        }, status_code=400)
    
    companies = load_google_sheets_data()
    if not companies:
        return JSONResponse({
            "status": "error",
            "message": "No data available"
        }, status_code=404)
    
    results = []
    for company in companies:
        for good in company['goods']:
            if good.get('Produced Goods', '').lower() == good_name.lower():
                results.append({
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
    
    if not results:
        return JSONResponse({
            "status": "error",
            "message": f"Good '{good_name}' not found"
        }, status_code=404)
    
    # Sort by guildees_pay (cheapest first)
    results.sort(key=lambda x: x['guildees_pay'])
    
    return JSONResponse({
        "status": "success",
        "query": {"good": good_name},
        "data": {
            "results": results,
            "count": len(results),
            "cheapest": results[0] if results else None
        }
    })


async def api_company_detail(request):
    """Get details for a specific company."""
    company_name = request.path_params.get('company_name')
    if not company_name:
        return JSONResponse({
            "status": "error",
            "message": "Company name is required"
        }, status_code=400)
    
    companies = load_google_sheets_data()
    if not companies:
        return JSONResponse({
            "status": "error",
            "message": "No data available"
        }, status_code=404)
    
    for company in companies:
        if company['name'].lower() == company_name.lower():
            # Format goods data
            goods_list = []
            for good in company['goods']:
                goods_list.append({
                    'produced_goods': good.get('Produced Goods', ''),
                    'planet_produced': good.get('Planet Produced', ''),
                    'guildees_pay': good.get('Guildees Pay:', 0),
                    'live_exc_price': good.get('Live EXC Price', 0),
                    'live_avg_price': good.get('Live AVG Price', 0),
                    'guild_max': good.get('Guild Max', 0),
                    'guild_min': good.get('Guild Min', 0),
                    'discount_percent': good.get('Guild % Discount', 0),
                    'discount_fixed': good.get('Guild Fixed Discount', 0)
                })
            
            return JSONResponse({
                "status": "success",
                "query": {"company": company_name},
                "data": {
                    "name": company['name'],
                    "industry": company['industry'],
                    "professions": company.get('professions', []),
                    "timezone": company.get('timezone', 'UTC +00:00'),
                    "local_time": company.get('local_time', 'N/A'),
                    "goods": goods_list
                }
            })
    
    return JSONResponse({
        "status": "error",
        "message": f"Company '{company_name}' not found"
    }, status_code=404)


async def api_all_data(request):
    """Get complete dataset."""
    companies = load_google_sheets_data()
    if not companies:
        return JSONResponse({
            "status": "error",
            "message": "No data available"
        }, status_code=404)
    
    # Format all data for JSON
    formatted_companies = []
    for company in companies:
        goods_list = []
        for good in company['goods']:
            goods_list.append({
                'produced_goods': good.get('Produced Goods', ''),
                'planet_produced': good.get('Planet Produced', ''),
                'guildees_pay': good.get('Guildees Pay:', 0),
                'live_exc_price': good.get('Live EXC Price', 0),
                'live_avg_price': good.get('Live AVG Price', 0),
                'guild_max': good.get('Guild Max', 0),
                'guild_min': good.get('Guild Min', 0),
                'discount_percent': good.get('Guild % Discount', 0),
                'discount_fixed': good.get('Guild Fixed Discount', 0)
            })
        
        formatted_companies.append({
            "name": company['name'],
            "industry": company['industry'],
            "professions": company.get('professions', []),
            "timezone": company.get('timezone', 'UTC +00:00'),
            "local_time": company.get('local_time', 'N/A'),
            "goods": goods_list
        })
    
    return JSONResponse({
        "status": "success",
        "data": {
            "companies": formatted_companies,
            "count": len(formatted_companies)
        }
    })


# Create the Streamlit app with custom API routes
app = App(
    "app.py",
    routes=[
        Route("/api/health", api_health),
        Route("/api/goods", api_goods_list),
        Route("/api/companies", api_companies_list),
        Route("/api/good/{good_name}", api_good_detail),
        Route("/api/company/{company_name}", api_company_detail),
        Route("/api/all", api_all_data),
    ],
)
