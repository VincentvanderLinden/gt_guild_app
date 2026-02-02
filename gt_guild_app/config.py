"""Configuration constants for the TiT Guild App."""
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
CSS_FILE = ASSETS_DIR / "css" / "style.css"
DATA_FILE = ASSETS_DIR / "data" / "guild_data.feather"
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
