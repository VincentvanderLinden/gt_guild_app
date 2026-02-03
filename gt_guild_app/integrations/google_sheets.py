"""Google Sheets integration for importing guild data."""
import requests
import pandas as pd
from typing import Optional
import re


def extract_sheet_id(url: str) -> Optional[str]:
    """Extract sheet ID from Google Sheets URL."""
    pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None


def extract_gid(url: str) -> Optional[str]:
    """Extract gid (sheet tab ID) from Google Sheets URL."""
    pattern = r'gid=(\d+)'
    match = re.search(pattern, url)
    return match.group(1) if match else '0'


def fetch_google_sheet(sheet_url: str) -> Optional[pd.DataFrame]:
    """
    Fetch data from a public Google Sheet.
    The sheet must be publicly accessible (Share > Anyone with the link can view).
    """
    sheet_id = extract_sheet_id(sheet_url)
    gid = extract_gid(sheet_url)
    
    if not sheet_id:
        return None
    
    # Construct CSV export URL
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    try:
        response = requests.get(csv_url, timeout=10)
        response.raise_for_status()
        
        # Parse CSV data
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        return df
    except Exception as e:
        print(f"Error fetching Google Sheet: {e}")
        return None


def parse_goods_column(goods_str: str) -> list:
    """Parse comma-separated goods into a list."""
    if pd.isna(goods_str) or not goods_str:
        return []
    
    # Split by comma or newline
    goods = [g.strip() for g in str(goods_str).replace('\n', ',').split(',')]
    return [g for g in goods if g]


def import_from_google_sheet(sheet_url: str) -> Optional[list]:
    """
    Import guild data from Google Sheet.
    
    Expected structure:
    - Row 28: Headers (Company Name, Timezone, etc.)
    - Row 29+: Data rows
    - Columns:
      * A: Company name
      * B: Industry/Professions (can be comma-separated, e.g., "Agriculture, Food Production")
      * C: Timezone
      * M: Produced Goods (one per row)
      * N: Planet Produced (ignores "Select Planet")
      * R: Guild Max
      * S: Guild Min
      * T: Guild % Discount
      * U: Guild Fixed Discount
    
    Returns list of company dictionaries.
    """
    df = fetch_google_sheet(sheet_url)
    
    if df is None:
        return None
    
    # Find the header row (contains "Company Name")
    header_row_idx = None
    for idx in range(min(50, len(df))):
        if pd.notna(df.iloc[idx, 0]) and str(df.iloc[idx, 0]).strip() == "Company Name":
            header_row_idx = idx
            break
    
    if header_row_idx is None:
        print("Could not find header row with 'Company Name' in column A")
        return None
    
    # Group goods by company
    companies_dict = {}
    current_company = None
    current_industry = None
    current_professions = []
    current_timezone = None
    
    # Iterate through data rows (starting after header)
    for idx in range(header_row_idx + 1, len(df)):
        try:
            company_name_cell = df.iloc[idx, 0] if len(df.iloc[idx]) > 0 else None  # Column A
            
            # Check if this is a header row (reset context)
            if pd.notna(company_name_cell) and str(company_name_cell).strip() == "Company Name":
                current_company = None
                current_industry = None
                current_professions = []
                current_timezone = None
                continue
            
            # Check if this row has a new company name
            if pd.notna(company_name_cell) and str(company_name_cell).strip():
                current_company = str(company_name_cell).strip()
                
                # Parse industry/professions (can be comma-separated)
                industry_str = str(df.iloc[idx, 1]).strip() if len(df.iloc[idx]) > 1 and pd.notna(df.iloc[idx, 1]) else "Unknown"  # Column B
                current_industry = industry_str
                
                # Parse professions - split by comma, newline, or &
                current_professions = []
                if industry_str and industry_str != "Unknown":
                    prof_list = industry_str.replace('\n', ',').replace('&', ',').replace(' and ', ',').split(',')
                    current_professions = [p.strip() for p in prof_list if p.strip() and p.strip().lower() not in ['select profession(s)', 'select profession', 'unknown']]
                
                current_timezone = str(df.iloc[idx, 2]).strip() if len(df.iloc[idx]) > 2 and pd.notna(df.iloc[idx, 2]) else "UTC +00:00"  # Column C
            
            # Skip if we don't have a current company context
            if not current_company:
                continue
            
            # Check for additional profession in column B (on rows where column A is empty)
            profession_cell = df.iloc[idx, 1] if len(df.iloc[idx]) > 1 else None  # Column B
            if pd.notna(profession_cell) and str(profession_cell).strip() and pd.isna(company_name_cell):
                # This is an additional profession for the current company
                prof = str(profession_cell).strip()
                # Skip placeholder text
                if prof not in current_professions and prof.lower() not in ['select profession(s)', 'select profession', 'unknown']:
                    current_professions.append(prof)
            
            company_name = current_company
            industry = current_industry
            professions = current_professions
            timezone = current_timezone
            
            # Get goods info for this row
            good_name = df.iloc[idx, 12] if len(df.iloc[idx]) > 12 else ""  # Column M (0-indexed: 12)
            planet_produced = df.iloc[idx, 13] if len(df.iloc[idx]) > 13 else ""  # Column N (0-indexed: 13)
            
            # Skip if no good name
            if pd.isna(good_name) or not str(good_name).strip():
                continue
            
            good_name = str(good_name).strip()
            
            # Parse planet produced, filter out placeholder
            if pd.notna(planet_produced):
                planet_produced = str(planet_produced).strip()
                if planet_produced.lower() == 'select planet':
                    planet_produced = ''
            else:
                planet_produced = ''
            
            # Get pricing info - remove $ signs and % signs
            def parse_price(val):
                if pd.isna(val):
                    return 0
                val_str = str(val).replace('$', '').replace('%', '').replace(',', '').strip()
                try:
                    return float(val_str) if val_str else 0
                except:
                    return 0
            
            guildees_pay = parse_price(df.iloc[idx, 14])  # Column O (0-indexed: 14)
            guild_max = parse_price(df.iloc[idx, 17])  # Column R (0-indexed: 17)
            guild_min = parse_price(df.iloc[idx, 18])  # Column S (0-indexed: 18)
            guild_discount = parse_price(df.iloc[idx, 19])  # Column T (0-indexed: 19)
            guild_fixed_discount = parse_price(df.iloc[idx, 20]) if len(df.iloc[idx]) > 20 else 0  # Column U (0-indexed: 20)
            
            # Initialize company entry if not exists
            if company_name not in companies_dict:
                companies_dict[company_name] = {
                    'name': company_name,
                    'industry': industry,
                    'professions': professions if professions else [industry],  # Use parsed professions or fall back to industry
                    'timezone': timezone,
                    'local_time': 'N/A',  # Will be calculated
                    'goods': []
                }
            
            # Add this good to the company
            companies_dict[company_name]['goods'].append({
                'Produced Goods': good_name,
                'Planet Produced': planet_produced,
                'Guildees Pay:': int(guildees_pay) if guildees_pay else 0,
                'Live EXC Price': 0,  # Will be updated from API
                'Live AVG Price': 0,  # Will be updated from API
                'Guild Max': int(guild_max),
                'Guild Min': int(guild_min),
                'Guild % Discount': int(guild_discount),
                'Guild Fixed Discount': int(guild_fixed_discount)
            })
        
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            continue
    
    # Convert dict to list
    companies = list(companies_dict.values())
    
    return companies if companies else None
