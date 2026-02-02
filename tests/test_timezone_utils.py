"""Tests for timezone utility functions."""
import pytest
from datetime import datetime
from gt_guild_app.integrations.timezone_utils import (
    parse_timezone_offset,
    get_local_time,
    update_company_local_times
)


class TestParseTimezoneOffset:
    """Tests for parse_timezone_offset function."""
    
    def test_positive_offset_with_minutes(self):
        """Test parsing positive offset with minutes"""
        assert parse_timezone_offset("UTC +05:30") == 330  # 5.5 hours in minutes
        assert parse_timezone_offset("UTC +01:00") == 60
    
    def test_negative_offset_with_minutes(self):
        """Test parsing negative offset with minutes"""
        assert parse_timezone_offset("UTC -05:00") == -300
        assert parse_timezone_offset("UTC -08:00") == -480
    
    def test_offset_without_minutes(self):
        """Test parsing offset without minute specification"""
        assert parse_timezone_offset("UTC +5") == 300
        assert parse_timezone_offset("UTC -7") == -420
    
    def test_utc_zero(self):
        """Test UTC +00:00"""
        assert parse_timezone_offset("UTC +00:00") == 0
        assert parse_timezone_offset("UTC +0") == 0
    
    def test_invalid_format(self):
        """Test handling of invalid formats"""
        assert parse_timezone_offset("") == 0
        assert parse_timezone_offset("invalid") == 0
        assert parse_timezone_offset(None) == 0


class TestGetLocalTime:
    """Tests for get_local_time function."""
    
    def test_returns_string(self):
        """Test that function returns a string"""
        result = get_local_time("UTC +00:00")
        assert isinstance(result, str)
    
    def test_time_format(self):
        """Test that returned time is in correct format"""
        result = get_local_time("UTC +00:00")
        # Should be in format like "2:30 PM" or "12:00 AM"
        assert ":" in result
        assert any(meridiem in result for meridiem in ["AM", "PM"])
    
    def test_different_timezones(self):
        """Test with different timezone offsets"""
        # Just ensure they return valid strings
        assert isinstance(get_local_time("UTC +05:00"), str)
        assert isinstance(get_local_time("UTC -08:00"), str)
        assert isinstance(get_local_time("UTC +12:00"), str)
    
    def test_invalid_timezone(self):
        """Test handling of invalid timezone"""
        result = get_local_time("invalid")
        assert result == "N/A"


class TestUpdateCompanyLocalTimes:
    """Tests for update_company_local_times function."""
    
    def test_update_single_company(self):
        """Test updating local time for a single company"""
        companies = [
            {
                'name': 'Test Co',
                'timezone': 'UTC +00:00',
                'local_time': 'N/A'
            }
        ]
        
        result = update_company_local_times(companies)
        
        assert result[0]['local_time'] != 'N/A'
        assert isinstance(result[0]['local_time'], str)
    
    def test_update_multiple_companies(self):
        """Test updating local times for multiple companies"""
        companies = [
            {'name': 'US Co', 'timezone': 'UTC -05:00', 'local_time': 'N/A'},
            {'name': 'UK Co', 'timezone': 'UTC +00:00', 'local_time': 'N/A'},
            {'name': 'India Co', 'timezone': 'UTC +05:30', 'local_time': 'N/A'}
        ]
        
        result = update_company_local_times(companies)
        
        for company in result:
            assert company['local_time'] != 'N/A'
            assert isinstance(company['local_time'], str)
    
    def test_preserves_other_fields(self):
        """Test that function doesn't modify other company fields"""
        companies = [
            {
                'name': 'Test Co',
                'industry': 'Manufacturing',
                'timezone': 'UTC +00:00',
                'local_time': 'N/A',
                'goods': []
            }
        ]
        
        result = update_company_local_times(companies)
        
        assert result[0]['name'] == 'Test Co'
        assert result[0]['industry'] == 'Manufacturing'
        assert result[0]['goods'] == []
