"""Timezone utilities for displaying local times."""
from datetime import datetime
import re


def parse_timezone_offset(timezone_str: str) -> int:
    """
    Parse timezone string to get UTC offset in minutes.
    Handles formats like: 'UTC +01:00', 'UTC-5', 'UTC +00:00', etc.
    """
    if not timezone_str:
        return 0
    
    # Extract the offset part (e.g., '+01:00' or '-5')
    pattern = r'UTC\s*([-+]?\d{1,2})(?::(\d{2}))?'
    match = re.search(pattern, str(timezone_str), re.IGNORECASE)
    
    if not match:
        return 0
    
    hours = int(match.group(1))
    minutes = int(match.group(2)) if match.group(2) else 0
    
    # Convert to total minutes
    total_minutes = hours * 60 + (minutes if hours >= 0 else -minutes)
    
    return total_minutes


def get_local_time(timezone_str: str) -> str:
    """
    Get current local time based on timezone string.
    Returns formatted time string like '2:30 PM'.
    """
    try:
        offset_minutes = parse_timezone_offset(timezone_str)
        
        # Get current UTC time
        utc_now = datetime.utcnow()
        
        # Add offset
        from datetime import timedelta
        local_time = utc_now + timedelta(minutes=offset_minutes)
        
        # Format as 12-hour time
        return local_time.strftime('%I:%M %p').lstrip('0')
    except Exception as e:
        return 'N/A'


def update_company_local_times(companies: list) -> list:
    """Update local_time field for all companies based on their timezone."""
    for company in companies:
        timezone = company.get('timezone', 'UTC +00:00')
        company['local_time'] = get_local_time(timezone)
    return companies
