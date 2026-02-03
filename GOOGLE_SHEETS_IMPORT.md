# Google Sheets Import

This app can import guild data directly from your Google Sheets spreadsheet.

## Setup

1. **Make your Google Sheet publicly accessible:**
   - Open your Google Sheet
   - Click "Share" button (top right)
   - Change to "Anyone with the link can view"
   - Copy the share link

2. **Update the sheet URL in `import_sheet.py`:**
   ```python
   SHEET_URL = "your_google_sheets_url_here"
   ```

3. **Run the import script:**
   ```bash
   python import_sheet.py
   ```

## Sheet Structure

The import script expects the following structure:

### Required Columns:
- **Column A:** Company Name
- **Column B:** Industry/Professions (can be comma-separated, e.g., "Agriculture, Food Production")
- **Column C:** Timezone (e.g., "UTC -07:00", "UTC +01:00")
- **Column M:** Produced Goods (one good per row)
- **Column R:** Guild Max (with or without $ signs)
- **Column S:** Guild Min (with or without $ signs)
- **Column T:** Guild % Discount (with or without % signs)
- **Column U:** Guild Fixed Discount (with or without $ signs)

### Multiple Professions:

You can list multiple professions in column B using any of these formats:
- **Comma-separated:** `Agriculture, Food Production`
- **Ampersand:** `Agriculture & Food Production`
- **"and" keyword:** `Agriculture and Food Production`
- **Newlines:** Multiple lines in the cell

The import script will automatically parse all formats and create a list of professions for each company.

### Notes:
- The script will automatically find the header row (looks for "Company Name" in column A)
- Each row represents one good from one company
- Multiple goods from the same company will be grouped together
- Companies without any goods will be skipped
- The "Local Time" column will be calculated automatically based on the timezone

## Timezone Format

Timezones should be in the format: `UTC ±HH:MM`

Examples:
- `UTC -07:00` (Pacific Time)
- `UTC +00:00` (GMT/UTC)
- `UTC +01:00` (Central European Time)
- `UTC -05:00` (Eastern Time)
- `UTC +09:00` (Japan)

## Price Format

Prices can include currency symbols and formatting:
- `$35.00` → 35
- `$1,234` → 1234
- `20%` → 20
- `500` → 500

## After Import

After running the import:
1. The data will be saved to `assets/data/guild_data.feather`
2. Open the Streamlit app
3. Set professions for each company (the import can't determine this automatically)
4. Live prices will be fetched from the API
5. Guildees Pay will be calculated based on Guild Max/Min and discounts

## Troubleshooting

### "Failed to fetch data from Google Sheet"
- Make sure the sheet is publicly accessible (Share > Anyone with the link can view)
- Check that the URL is correct

### "Could not find header row"
- Make sure there's a row with "Company Name" in column A
- The header should be within the first 50 rows

### "No valid company data found"
- Check that companies have both a company name (column A) and at least one good (column M)
- Make sure the data isn't using "Company Name" as placeholder text

## Automatic Updates

The local times are automatically recalculated every time you load the app, so they'll always show the current time in each company's timezone.

To refresh the data from Google Sheets:
```bash
python import_sheet.py
```

Then restart your Streamlit app to see the updated data.
