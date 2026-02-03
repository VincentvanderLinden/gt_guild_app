"""Configuration constants for the TiT Guild App."""
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
CSS_FILE = ASSETS_DIR / "css" / "style.css"
DATA_FILE = ASSETS_DIR / "data" / "guild_data.feather"
GOOGLE_SHEETS_DATA_FILE = ASSETS_DIR / "data" / "google_sheets_data.feather"
GAMEDATA_FILE = ASSETS_DIR / "data" / "gamedata.json"

# Available professions (sorted alphabetically)
PROFESSIONS = sorted([
    "Construction",
    "Manufacturing",
    "Agriculture",
    "Resource Extraction",
    "Metallurgy",
    "Chemistry",
    "Electronics",
    "Food Production",
    "Science",
    "Chicken Farmer",
    "ConstRICtion",
    "Transporting",
    "Jack-of-all-Trades",
    "Failing Hard"
])

# App settings
APP_TITLE = "TiT Guild App™"
APP_ICON = "🐔"
APP_SUBTITLE = "*View and manage items that players are selling*"

# Timezone options with city names
TIMEZONE_OPTIONS = [
    "UTC -12:00 (Baker Island)",
    "UTC -11:00 (American Samoa)",
    "UTC -10:00 (Hawaii)",
    "UTC -09:00 (Alaska)",
    "UTC -08:00 (Los Angeles, Vancouver)",
    "UTC -07:00 (Denver, Phoenix)",
    "UTC -06:00 (Chicago, Mexico City)",
    "UTC -05:00 (New York, Toronto)",
    "UTC -04:00 (Santiago, Halifax)",
    "UTC -03:00 (Buenos Aires, São Paulo)",
    "UTC -02:00 (South Georgia)",
    "UTC -01:00 (Azores)",
    "UTC +00:00 (London, Lisbon)",
    "UTC +01:00 (Paris, Berlin, Rome)",
    "UTC +02:00 (Athens, Cairo, Helsinki)",
    "UTC +03:00 (Moscow, Istanbul, Nairobi)",
    "UTC +04:00 (Dubai, Baku)",
    "UTC +05:00 (Karachi, Tashkent)",
    "UTC +05:30 (Mumbai, Delhi)",
    "UTC +06:00 (Dhaka, Almaty)",
    "UTC +07:00 (Bangkok, Jakarta)",
    "UTC +08:00 (Beijing, Singapore, Perth)",
    "UTC +09:00 (Tokyo, Seoul)",
    "UTC +09:30 (Adelaide)",
    "UTC +10:00 (Sydney, Melbourne)",
    "UTC +11:00 (Solomon Islands)",
    "UTC +12:00 (Auckland, Fiji)",
    "UTC +13:00 (Tonga)",
    "UTC +14:00 (Kiribati)",
]
