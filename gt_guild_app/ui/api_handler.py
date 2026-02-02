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
    st.title("🔌 API Documentation")
    st.markdown("Access guild pricing data via URL parameters.")
    
    st.divider()
    
    st.header("Endpoints")
    
    st.subheader("1. Find Cheapest Price for a Good")
    st.code("?good=<good_name>[&format=json]", language="bash")
    st.markdown("**Example:**")
    st.code("?good=Steel&format=json", language="bash")
    st.markdown("Returns the cheapest guildee price across all companies for the specified good.")
    
    st.divider()
    
    st.subheader("2. Get Company Goods")
    st.code("?company=<company_name>[&format=json]", language="bash")
    st.markdown("**Example:**")
    st.code("?company=Flip Co&format=json", language="bash")
    st.markdown("Returns all goods sold by the specified company.")
    
    st.divider()
    
    st.subheader("3. List All Goods")
    st.code("?list=goods[&format=json]", language="bash")
    st.markdown("Returns a list of all unique goods available.")
    
    st.divider()
    
    st.subheader("4. List All Companies")
    st.code("?list=companies[&format=json]", language="bash")
    st.markdown("Returns a list of all companies with their basic info.")
    
    st.divider()
    
    st.header("Response Formats")
    st.markdown("""
    - **HTML (default)**: User-friendly display with tables and metrics
    - **JSON**: Add `&format=json` to any query for JSON output
    """)
    
    st.divider()
    
    st.header("Examples")
    
    base_url = st.query_params.get("_base_url", "your-app-url.streamlit.app")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**HTML Responses:**")
        st.code(f"""
# Get cheapest Steel
{base_url}?good=Steel

# Get Flip Co's goods
{base_url}?company=Flip Co

# List all goods
{base_url}?list=goods
        """.strip(), language="bash")
    
    with col2:
        st.markdown("**JSON Responses:**")
        st.code(f"""
# Get cheapest Steel (JSON)
{base_url}?good=Steel&format=json

# Get Flip Co's goods (JSON)
{base_url}?company=Flip Co&format=json

# List all goods (JSON)
{base_url}?list=goods&format=json
        """.strip(), language="bash")
