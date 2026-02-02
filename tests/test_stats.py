"""Tests for statistics calculation functions."""
import pytest
from gt_guild_app.business.stats import (
    calculate_unique_goods,
    calculate_average_discount,
    get_unique_professions
)


class TestCalculateUniqueGoods:
    """Tests for calculate_unique_goods function."""
    
    def test_single_company(self):
        """Test counting unique goods from single company"""
        companies = [
            {
                'name': 'Co1',
                'goods': [
                    {'Produced Goods': 'Steel'},
                    {'Produced Goods': 'Iron'}
                ]
            }
        ]
        
        result = calculate_unique_goods(companies)
        
        assert result == 2
    
    def test_multiple_companies_unique(self):
        """Test with multiple companies, all unique goods"""
        companies = [
            {'name': 'Co1', 'goods': [{'Produced Goods': 'Steel'}]},
            {'name': 'Co2', 'goods': [{'Produced Goods': 'Iron'}]},
            {'name': 'Co3', 'goods': [{'Produced Goods': 'Copper'}]}
        ]
        
        result = calculate_unique_goods(companies)
        
        assert result == 3
    
    def test_multiple_companies_duplicates(self):
        """Test with duplicate goods across companies"""
        companies = [
            {'name': 'Co1', 'goods': [{'Produced Goods': 'Steel'}]},
            {'name': 'Co2', 'goods': [{'Produced Goods': 'Steel'}]},
            {'name': 'Co3', 'goods': [{'Produced Goods': 'Iron'}]}
        ]
        
        result = calculate_unique_goods(companies)
        
        assert result == 2
    
    def test_empty_companies(self):
        """Test with empty companies list"""
        companies = []
        
        result = calculate_unique_goods(companies)
        
        assert result == 0
    
    def test_company_with_no_goods(self):
        """Test with company having empty goods list"""
        companies = [
            {'name': 'Co1', 'goods': []}
        ]
        
        result = calculate_unique_goods(companies)
        
        assert result == 0


class TestCalculateAverageDiscount:
    """Tests for calculate_average_discount function."""
    
    def test_single_company(self):
        """Test average discount for single company"""
        companies = [
            {
                'name': 'Co1',
                'goods': [
                    {'Guild % Discount': 10},
                    {'Guild % Discount': 20}
                ]
            }
        ]
        
        result = calculate_average_discount(companies)
        
        assert result == 15.0
    
    def test_multiple_companies(self):
        """Test average across multiple companies"""
        companies = [
            {'name': 'Co1', 'goods': [{'Guild % Discount': 10}]},
            {'name': 'Co2', 'goods': [{'Guild % Discount': 20}]},
            {'name': 'Co3', 'goods': [{'Guild % Discount': 30}]}
        ]
        
        result = calculate_average_discount(companies)
        
        assert result == 20.0
    
    def test_zero_discounts(self):
        """Test with all zero discounts"""
        companies = [
            {'name': 'Co1', 'goods': [{'Guild % Discount': 0}]},
            {'name': 'Co2', 'goods': [{'Guild % Discount': 0}]}
        ]
        
        result = calculate_average_discount(companies)
        
        assert result == 0.0
    
    def test_empty_companies(self):
        """Test with empty companies list"""
        companies = []
        
        result = calculate_average_discount(companies)
        
        assert result == 0.0
    
    def test_mixed_discounts(self):
        """Test with various discount values"""
        companies = [
            {'name': 'Co1', 'goods': [
                {'Guild % Discount': 5},
                {'Guild % Discount': 15},
                {'Guild % Discount': 25}
            ]}
        ]
        
        result = calculate_average_discount(companies)
        
        assert result == 15.0


class TestGetUniqueProfessions:
    """Tests for get_unique_professions function."""
    
    def test_single_company_single_profession(self):
        """Test with one company having one profession"""
        companies = [
            {'name': 'Co1', 'professions': ['Agriculture']}
        ]
        
        result = get_unique_professions(companies)
        
        assert result == {'Agriculture'}
    
    def test_single_company_multiple_professions(self):
        """Test with one company having multiple professions"""
        companies = [
            {'name': 'Co1', 'professions': ['Agriculture', 'Food Production']}
        ]
        
        result = get_unique_professions(companies)
        
        assert result == {'Agriculture', 'Food Production'}
    
    def test_multiple_companies_unique(self):
        """Test with multiple companies, all unique professions"""
        companies = [
            {'name': 'Co1', 'professions': ['Agriculture']},
            {'name': 'Co2', 'professions': ['Metallurgy']},
            {'name': 'Co3', 'professions': ['Manufacturing']}
        ]
        
        result = get_unique_professions(companies)
        
        assert result == {'Agriculture', 'Metallurgy', 'Manufacturing'}
    
    def test_multiple_companies_duplicates(self):
        """Test with duplicate professions across companies"""
        companies = [
            {'name': 'Co1', 'professions': ['Agriculture', 'Food Production']},
            {'name': 'Co2', 'professions': ['Agriculture']},
            {'name': 'Co3', 'professions': ['Metallurgy']}
        ]
        
        result = get_unique_professions(companies)
        
        assert result == {'Agriculture', 'Food Production', 'Metallurgy'}
    
    def test_empty_companies(self):
        """Test with empty companies list"""
        companies = []
        
        result = get_unique_professions(companies)
        
        assert result == set()
    
    def test_company_with_empty_professions(self):
        """Test with company having empty professions list"""
        companies = [
            {'name': 'Co1', 'professions': []},
            {'name': 'Co2', 'professions': ['Metallurgy']}
        ]
        
        result = get_unique_professions(companies)
        
        assert result == {'Metallurgy'}
