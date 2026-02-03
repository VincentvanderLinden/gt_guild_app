"""API query handlers for URL parameter access."""
import streamlit as st
import json
import pandas as pd
from typing import List, Dict, Any, Optional


def format_json_response(data: Dict[str, Any], status: str = "success") -> Dict[str, Any]:
    """Format response with metadata for easier scraping."""
    return {
        "status": status,
        "timestamp": pd.Timestamp.now(tz="UTC").isoformat(),
        "data": data
    }


def render_json_response(data: Dict[str, Any]):
    """Render JSON response with proper content type and formatting."""
    # Set content type for JSON
    st.set_page_config(page_title="API Response", page_icon="🔌")
    
    # Display formatted JSON with custom class for scraping
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    st.markdown(
        f'<p class="look_here_flip" style="white-space: pre-wrap; font-family: monospace;">{json_str}</p>',
        unsafe_allow_html=True
    )


def get_cheapest_price_for_good(companies: List[Dict[str, Any]], good_name: str) -> Optional[Dict[str, Any]]:
    """Find the cheapest guildee price for a specific good across all companies."""
    results = []
    
    for company in companies:
        for good in company['goods']:
            if good.get('Produced Goods', '').lower() == good_name.lower():
                results.append({
                    'company': company['name'],
                    'good': good.get('Produced Goods', ''),
                    'guildees_pay': good.get('Guildees Pay:', 0),
                    'live_exc_price': good.get('Live EXC Price', 0),
                    'live_avg_price': good.get('Live AVG Price', 0),
                    'guild_max': good.get('Guild Max', 0),
                    'guild_min': good.get('Guild Min', 0),
                    'discount_percent': good.get('Guild % Discount', 0),
                    'discount_fixed': good.get('Guild Fixed Discount', 0),
                    'timezone': company['timezone'],
                    'professions': company.get('professions', [])
                })
    
    if not results:
        return None
    
    # Sort by guildees_pay (cheapest first)
    results.sort(key=lambda x: x['guildees_pay'])
    
    return {
        'good_name': good_name,
        'cheapest_price': results[0]['guildees_pay'],
        'cheapest_company': results[0]['company'],
        'all_offers': results
    }


def get_company_goods(companies: List[Dict[str, Any]], company_name: str) -> Optional[Dict[str, Any]]:
    """Get all goods for a specific company."""
    for company in companies:
        if company['name'].lower() == company_name.lower():
            return {
                'company_name': company['name'],
                'professions': company.get('professions', []),
                'timezone': company['timezone'],
                'local_time': company['local_time'],
                'goods': company['goods']
            }
    return None


def render_api_response(query_params: Dict[str, Any], companies: List[Dict[str, Any]]):
    """Render API response based on query parameters."""
    # Get format preference (json or default HTML)
    output_format = query_params.get('format', 'html')
    if isinstance(output_format, list):
        output_format = output_format[0]
    output_format = output_format.lower()
    
    # Handle 'good' query
    if 'good' in query_params:
        good_name = query_params['good']
        if isinstance(good_name, list):
            good_name = good_name[0]
        
        result = get_cheapest_price_for_good(companies, good_name)
        
        if result is None:
            if output_format == 'json':
                error_response = format_json_response(
                    {"error": f"Good '{good_name}' not found"},
                    status="error"
                )
                render_json_response(error_response)
            else:
                st.error(f"❌ Good '{good_name}' not found in any company")
            return True
        
        if output_format == 'json':
            response = format_json_response({
                "query": {
                    "type": "good",
                    "good_name": good_name
                },
                "result": result
            })
            render_json_response(response)
        else:
            st.title(f"🔍 Cheapest Price for: {result['good_name']}")
            st.metric(
                "Best Price", 
                f"${result['cheapest_price']:.2f}",
                f"from {result['cheapest_company']}"
            )
            
            st.divider()
            st.subheader("All Offers")
            
            # Create comparison table
            df = pd.DataFrame(result['all_offers'])
            df = df[['company', 'guildees_pay', 'live_exc_price', 'discount_percent', 'guild_min', 'guild_max']]
            df.columns = ['Company', 'Guildees Pay', 'Live EXC Price', 'Discount %', 'Min', 'Max']
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.info("💡 **API Usage:**\n- JSON: Add `&format=json` to URL\n- Example: `?good=Steel&format=json`")
        
        return True
    
    # Handle 'company' query
    if 'company' in query_params:
        company_name = query_params['company']
        if isinstance(company_name, list):
            company_name = company_name[0]
        
        result = get_company_goods(companies, company_name)
        
        if result is None:
            if output_format == 'json':
                error_response = format_json_response(
                    {"error": f"Company '{company_name}' not found"},
                    status="error"
                )
                render_json_response(error_response)
            else:
                st.error(f"❌ Company '{company_name}' not found")
            return True
        
        if output_format == 'json':
            response = format_json_response({
                "query": {
                    "type": "company",
                    "company_name": company_name
                },
                "result": result
            })
            render_json_response(response)
        else:
            st.title(f"🏢 {result['company_name']}")
            st.caption(f"{', '.join(result['professions'])} | {result['timezone']} ({result['local_time']})")
            
            st.divider()
            st.subheader("Available Goods")
            
            df = pd.DataFrame(result['goods'])
            if not df.empty:
                df = df[['Produced Goods', 'Guildees Pay:', 'Live EXC Price', 'Guild % Discount', 'Guild Min', 'Guild Max']]
                df.columns = ['Good', 'Guildees Pay', 'Live EXC', 'Discount %', 'Min', 'Max']
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.info("💡 **API Usage:**\n- JSON: Add `&format=json` to URL\n- Example: `?company=Flip Co&format=json`")
        
        return True
    
    # Handle 'list' query (list all goods or companies)
    if 'list' in query_params:
        list_type = query_params['list']
        if isinstance(list_type, list):
            list_type = list_type[0]
        list_type = list_type.lower()
        
        if list_type == 'goods':
            all_goods = set()
            for company in companies:
                for good in company['goods']:
                    good_name = good.get('Produced Goods', '')
                    if good_name:
                        all_goods.add(good_name)
            
            result = {'goods': sorted(list(all_goods)), 'count': len(all_goods)}
            
            if output_format == 'json':
                response = format_json_response({
                    "query": {
                        "type": "list",
                        "list_type": "goods"
                    },
                    "result": result
                })
                render_json_response(response)
            else:
                st.title("📦 All Available Goods")
                st.write(f"Total: {len(result['goods'])} unique goods")
                st.dataframe(pd.DataFrame(result['goods'], columns=['Good Name']), use_container_width=True, hide_index=True)
            
            return True
        
        elif list_type == 'companies':
            company_list = [
                {
                    'name': c['name'],
                    'professions': c.get('professions', []),
                    'timezone': c['timezone'],
                    'goods_count': len(c['goods'])
                }
                for c in companies
            ]
            
            result = {'companies': company_list, 'count': len(company_list)}
            
            if output_format == 'json':
                response = format_json_response({
                    "query": {
                        "type": "list",
                        "list_type": "companies"
                    },
                    "result": result
                })
                render_json_response(response)
            else:
                st.title("🏢 All Companies")
                df = pd.DataFrame(company_list)
                df.columns = ['Company', 'Professions', 'Timezone', 'Goods Count']
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            return True
    
    return False


def show_api_documentation():
    """Show API documentation page."""
    st.title("🔌 REST API Documentation")
    st.markdown("Access guild pricing data via REST API endpoints for easy integration and scraping.")
    
    st.info("💡 **Run the app with**: `streamlit run gt_guild_app/main.py --server.port 8503`")
    
    st.divider()
    
    st.header("Available Endpoints")
    
    # Health Check
    st.subheader("1. Health Check")
    st.code("GET /api/health", language="http")
    st.markdown("Check if the API is running.")
    with st.expander("📋 Response Example"):
        st.json({
            "status": "healthy",
            "service": "TiT Guild App API"
        })
    
    st.divider()
    
    # List Goods
    st.subheader("2. List All Goods")
    st.code("GET /api/goods", language="http")
    st.markdown("Get a list of all unique goods across all companies.")
    with st.expander("📋 Response Example"):
        st.json({
            "status": "success",
            "data": {
                "goods": ["Adhesive", "Aluminum", "Steel", "..."],
                "count": 150
            }
        })
    
    st.divider()
    
    # List Companies
    st.subheader("3. List All Companies")
    st.code("GET /api/companies", language="http")
    st.markdown("Get a summary of all companies.")
    with st.expander("📋 Response Example"):
        st.json({
            "status": "success",
            "data": {
                "companies": [{
                    "name": "Company Name",
                    "industry": "Industry Type",
                    "professions": ["Prof1", "Prof2"],
                    "timezone": "UTC +00:00",
                    "goods_count": 25
                }],
                "count": 10
            }
        })
    
    st.divider()
    
    # Good Details
    st.subheader("4. Get Good Details")
    st.code("GET /api/good/{good_name}", language="http")
    st.markdown("Get pricing details for a specific good across all companies (sorted by cheapest).")
    st.markdown("**Example:** `/api/good/Steel`")
    with st.expander("📋 Response Example"):
        st.json({
            "status": "success",
            "query": {"good": "Steel"},
            "data": {
                "results": [{
                    "company": "Company Name",
                    "good": "Steel",
                    "planet_produced": "Kentaurus 2",
                    "guildees_pay": 100,
                    "live_exc_price": 120,
                    "guild_max": 110,
                    "discount_percent": 10,
                    "timezone": "UTC +00:00"
                }],
                "count": 5,
                "cheapest": {"company": "Best Co", "guildees_pay": 95}
            }
        })
    
    st.divider()
    
    # Company Details
    st.subheader("5. Get Company Details")
    st.code("GET /api/company/{company_name}", language="http")
    st.markdown("Get full details for a specific company with all goods.")
    st.markdown("**Example:** `/api/company/Flip Co`")
    with st.expander("📋 Response Example"):
        st.json({
            "status": "success",
            "query": {"company": "Flip Co"},
            "data": {
                "name": "Flip Co",
                "industry": "Mining",
                "professions": ["Miner"],
                "timezone": "UTC +01:00",
                "goods": [{"produced_goods": "Steel", "guildees_pay": 100}]
            }
        })
    
    st.divider()
    
    # All Data
    st.subheader("6. Get All Data")
    st.code("GET /api/all", language="http")
    st.markdown("Get the complete dataset with all companies and their goods.")
    st.warning("⚠️ Large response - use sparingly")
    
    st.divider()
    
    st.header("Usage Examples")
    
    tab1, tab2, tab3 = st.tabs(["Python", "cURL", "JavaScript"])
    
    with tab1:
        st.code("""
import requests

# Get health status
response = requests.get("http://localhost:8503/api/health")
print(response.json())

# Find cheapest steel
response = requests.get("http://localhost:8503/api/good/Steel")
data = response.json()
if data['status'] == 'success':
    cheapest = data['data']['cheapest']
    print(f"Cheapest at {cheapest['company']}: {cheapest['guildees_pay']}")

# Get all companies
response = requests.get("http://localhost:8503/api/companies")
companies = response.json()['data']['companies']
for company in companies:
    print(f"{company['name']} - {company['goods_count']} goods")
        """.strip(), language="python")
    
    with tab2:
        st.code("""
# Health check
curl http://localhost:8503/api/health

# Get all goods
curl http://localhost:8503/api/goods

# Get steel pricing
curl http://localhost:8503/api/good/Steel

# Get company details (use %20 for spaces)
curl http://localhost:8503/api/company/Flip%20Co

# Get all data
curl http://localhost:8503/api/all
        """.strip(), language="bash")
    
    with tab3:
        st.code("""
// Fetch all companies
fetch('http://localhost:8503/api/companies')
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      console.log(`Found ${data.data.count} companies`);
      data.data.companies.forEach(company => {
        console.log(`${company.name} - ${company.goods_count} goods`);
      });
    }
  });

// Find cheapest steel
fetch('http://localhost:8503/api/good/Steel')
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      const cheapest = data.data.cheapest;
      console.log(`Cheapest Steel: ${cheapest.company} at ${cheapest.guildees_pay}`);
    }
  });
        """.strip(), language="javascript")
    
    st.divider()
    
    st.header("Error Handling")
    st.markdown("""
    All endpoints return a consistent error format:
    
    ```json
    {
      "status": "error",
      "message": "Error description"
    }
    ```
    
    **HTTP Status Codes:**
    - `200`: Success
    - `400`: Bad Request (missing parameters)
    - `404`: Not Found (resource doesn't exist)
    - `500`: Internal Server Error
    """)
    
    st.divider()
    
    st.header("Implementation Details")
    st.markdown("""
    The API is built using Streamlit 1.53+'s native Starlette integration:
    
    ```python
    from streamlit.starlette import App
    from starlette.routing import Route
    from starlette.responses import JSONResponse
    
    app = App(
        "app.py",
        routes=[
            Route("/api/health", api_health),
            Route("/api/goods", api_goods_list),
            # ... more routes
        ],
    )
    ```
    
    This allows the same application to serve both the Streamlit UI and REST API endpoints.
    """)
    
    st.success("📖 Full documentation available in [API.md](https://github.com/yourusername/gt_guild_app/blob/main/API.md)")
