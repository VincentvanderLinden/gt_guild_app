"""Script to import data from Google Sheets and update guild_data.feather."""
import sys
from pathlib import Path

# Add gt_guild_app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'gt_guild_app'))

from integrations.google_sheets import import_from_google_sheet
from core.data_manager import save_data
from integrations.timezone_utils import update_company_local_times

# Google Sheet URL
from config import GOOGLE_SHEET_URL

SHEET_URL = GOOGLE_SHEET_URL


def main():
    """Import data from Google Sheet and save to feather file."""
    print("Fetching data from Google Sheet...")
    print(f"URL: {SHEET_URL}")
    print("\nNote: The sheet must be publicly accessible (Share > Anyone with the link can view)")
    print()
    
    companies = import_from_google_sheet(SHEET_URL)
    
    if companies is None:
        print("❌ Failed to fetch data from Google Sheet")
        print("   Make sure the sheet is publicly accessible")
        return
    
    if not companies:
        print("⚠️  No valid company data found in the sheet")
        return
    
    print(f"✅ Successfully imported {len(companies)} companies")
    print()
    
    # Update local times
    companies = update_company_local_times(companies)
    
    # Display summary
    print("Companies imported:")
    for company in companies:
        goods_count = len(company['goods'])
        print(f"  - {company['name']}: {goods_count} goods")
    
    print()
    
    # Save to feather
    try:
        save_data(companies)
        print("✅ Data saved to guild_data.feather")
        print()
        print("Note: You'll need to manually set professions for each company in the app")
    except Exception as e:
        print(f"❌ Error saving data: {e}")


if __name__ == "__main__":
    main()
