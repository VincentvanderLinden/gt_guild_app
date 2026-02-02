![TiT Guild App Banner](https://pasteimg.com/images/2026/01/24/image_2026-01-24_190453510.png)

# 🐔 TiT Guild App™

A comprehensive web application for managing guild trading data in Galactic Tycoons, featuring live price tracking, Google Sheets integration, and an intuitive interface for managing company goods and pricing.

## ✨ Features

### 🔄 Live Price Integration
- **Real-time Exchange Prices**: Fetches current material prices from Galactic Tycoons API
- **Auto-refresh**: Updates every 10 minutes with timestamp tracking
- **Smart Price Calculation**: Automatic guildee price calculation with 7-tier smart rounding system

### 📊 Google Sheets Sync
- **Automatic Import**: Syncs guild data from Google Sheets every 10 minutes
- **Multi-row Support**: Handles companies with multiple goods and professions
- **Timezone Aware**: Displays local times for each company based on timezone settings

### 🎯 Advanced Filtering
- **Profession Filter**: Filter companies by profession(s)
- **Company Search**: Quick search by company name
- **Material Search**: Find companies selling specific goods (filters both companies and data rows)

### 💼 Company Management
- **Dynamic Data Editor**: Add, edit, and delete goods with real-time validation
- **Profession Assignment**: Multi-select professions per company
- **Timezone Selection**: 30+ timezone options with city names (UTC -12:00 to +14:00)
- **Discount Configuration**: Set min/max prices and discount percentages

### 🌐 API Access
Programmatic access via URL parameters:
- `?good=Steel&format=json` - Get cheapest price for a material
- `?company=Flip%20Co&format=json` - Get all goods from a company
- `?list=goods` - List all available goods
- `?list=companies` - List all companies
- `?api` - View full API documentation

### 📈 Statistics Dashboard
- **Total Companies**: Count of active companies
- **Total Goods**: Unique goods across all companies
- **Active Professions**: Number of unique professions
- **Average Discount**: Mean discount percentage

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Poetry (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gt_guild_app
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Configure Google Sheets** (Optional)
   
   Update the Google Sheets URL in `gt_guild_app/config.py`:
   ```python
   GOOGLE_SHEET_URL = "your-google-sheets-export-url"
   ```

4. **Run the application**
   ```bash
   poetry run streamlit run gt_guild_app/app.py
   ```

5. **Access the app**
   
   Open your browser to `http://localhost:8501`

## 🏗️ Project Structure

```
gt_guild_app/
├── gt_guild_app/
│   ├── app.py                    # Main Streamlit application
│   ├── config.py                 # Configuration constants
│   │
│   ├── core/                     # Core data management
│   │   ├── data_manager.py       # Data loading/saving (feather format)
│   │   └── validators.py         # Data validation logic
│   │
│   ├── integrations/             # External system integrations
│   │   ├── api_client.py         # Galactic Tycoons API client
│   │   ├── google_sheets.py      # Google Sheets import
│   │   └── timezone_utils.py     # Timezone calculations
│   │
│   ├── business/                 # Business logic
│   │   ├── price_calculator.py   # Smart pricing & rounding
│   │   ├── stats.py              # Statistics calculations
│   │   └── filters.py            # Data filtering
│   │
│   ├── ui/                       # User interface components
│   │   ├── ui_components.py      # Reusable Streamlit components
│   │   └── api_handler.py        # API endpoint handlers
│   │
│   └── assets/                   # Static files
│       ├── css/style.css         # Custom styling
│       └── data/                 # Data files
│           ├── guild_data.feather
│           └── gamedata.json
│
├── scripts/                      # Utility scripts
│   └── import_sheet.py           # Manual Google Sheets import
│
├── tests/                        # Test suite
│   ├── test_price_calculator.py
│   ├── test_timezone_utils.py
│   ├── test_filters.py
│   ├── test_data_manager.py
│   └── test_stats.py
│
├── pyproject.toml                # Poetry dependencies
└── README.md                     # This file
```

## 🧪 Testing

Run the test suite:

```bash
poetry run pytest tests/
```

Run with coverage:

```bash
poetry run pytest tests/ --cov=gt_guild_app
```

## 💡 Usage

### Managing Company Data

1. **Add a Company**: Click "Add New Company" (if available) or edit existing companies
2. **Select Professions**: Use the multi-select dropdown to assign professions
3. **Set Timezone**: Choose from 30+ timezone options with recognizable city names
4. **Add Goods**: Use the dynamic data editor to add rows for each good
5. **Configure Pricing**: Set discount percentages, min/max bounds

### Price Calculation

The app uses a **7-tier smart rounding system**:
- Under $100: Rounds to nearest $0.50
- $100-$500: Rounds to nearest $1
- $500-$1,000: Rounds to nearest $5
- $1,000-$5,000: Rounds to nearest $10
- $5,000-$10,000: Rounds to nearest $50
- $10,000-$50,000: Rounds to nearest $100
- Over $50,000: Rounds to nearest $500

**Formula**: `Guildee Price = smart_round(Live Price × (1 - Discount%/100))`

Then applies min/max bounds if configured.

### Google Sheets Format

Expected columns:
- **Column A**: Company Name (appears once, carried forward)
- **Column B**: Professions (can span multiple rows)
- **Column C**: Timezone (UTC format, e.g., "UTC +01:00")
- **Column M**: Produced Goods
- **Column R**: Guild Max
- **Column S**: Guild Min
- **Column T**: Guild % Discount

Header row should be at row 28.

### API Examples

**Get cheapest price for Steel:**
```bash
curl "http://localhost:8501/?good=Steel&format=json"
```

**Get all goods from Flip Co:**
```bash
curl "http://localhost:8501/?company=Flip%20Co&format=json"
```

**List all available goods:**
```bash
curl "http://localhost:8501/?list=goods"
```

## 🎨 Theme

The app features a custom dark theme with:
- **Consistent styling** across light and dark mode settings
- **Titillium Web font** throughout
- **Blue accent colors** (#4a9eff) for headers and metrics
- **Patterned background** for visual interest
- **Custom data editor styling** with highlighted Guildee Pay column

## 🔧 Configuration

Key settings in `gt_guild_app/config.py`:

```python
# App settings
APP_TITLE = "TiT Guild App™"
APP_ICON = "🐔"

# Google Sheets URL
GOOGLE_SHEET_URL = "your-sheet-export-url"

# Professions list
PROFESSIONS = [...]

# Timezone options
TIMEZONE_OPTIONS = [...]
```

## 📝 Data Storage

- **Format**: Apache Feather (efficient columnar storage)
- **Location**: `gt_guild_app/assets/data/guild_data.feather`
- **Auto-save**: All changes saved automatically
- **Structure**: Flattened rows (one per company-good pair)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Galactic Tycoons** - Game and API
- **Streamlit** - Web framework
- **Apache Arrow** - Feather file format

---

Made with 🐔 for the TiT Guild