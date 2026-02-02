"""Tests for data filtering functions."""
import pytest
from gt_guild_app.business.filters import (
    filter_by_professions,
    filter_by_company_name,
    filter_by_goods_name,
    apply_all_filters
)


class TestFilterByProfessions:
    """Tests for filter_by_professions function."""
    
    def test_filter_single_profession(self):
        """Test filtering by a single profession"""
        companies = [
            {'name': 'Co1', 'professions': ['Agriculture', 'Food Production']},
            {'name': 'Co2', 'professions': ['Metallurgy']},
            {'name': 'Co3', 'professions': ['Agriculture']}
        ]
        
        result = filter_by_professions(companies, ['Agriculture'])
        
        assert len(result) == 2
        assert result[0]['name'] == 'Co1'
        assert result[1]['name'] == 'Co3'
    
    def test_filter_multiple_professions(self):
        """Test filtering by multiple professions"""
        companies = [
            {'name': 'Co1', 'professions': ['Agriculture']},
            {'name': 'Co2', 'professions': ['Metallurgy']},
            {'name': 'Co3', 'professions': ['Manufacturing']}
        ]
        
        result = filter_by_professions(companies, ['Agriculture', 'Metallurgy'])
        
        assert len(result) == 2
    
    def test_no_filter(self):
        """Test with empty profession list returns all"""
        companies = [
            {'name': 'Co1', 'professions': ['Agriculture']},
            {'name': 'Co2', 'professions': ['Metallurgy']}
        ]
        
        result = filter_by_professions(companies, [])
        
        assert len(result) == 2


class TestFilterByCompanyName:
    """Tests for filter_by_company_name function."""
    
    def test_exact_match(self):
        """Test filtering with exact company name"""
        companies = [
            {'name': 'Flip Co'},
            {'name': 'Skunk Industries'},
            {'name': 'Caboose Inc.'}
        ]
        
        result = filter_by_company_name(companies, 'Flip Co')
        
        assert len(result) == 1
        assert result[0]['name'] == 'Flip Co'
    
    def test_partial_match(self):
        """Test filtering with partial name"""
        companies = [
            {'name': 'Flip Co'},
            {'name': 'Skunk Industries'},
            {'name': 'Caboose Inc.'}
        ]
        
        result = filter_by_company_name(companies, 'Inc')
        
        assert len(result) == 1
        assert result[0]['name'] == 'Caboose Inc.'
    
    def test_case_insensitive(self):
        """Test that filtering is case-insensitive"""
        companies = [
            {'name': 'Flip Co'},
            {'name': 'SKUNK Industries'}
        ]
        
        result = filter_by_company_name(companies, 'flip')
        
        assert len(result) == 1
        assert result[0]['name'] == 'Flip Co'
    
    def test_no_filter(self):
        """Test with empty search term returns all"""
        companies = [
            {'name': 'Flip Co'},
            {'name': 'Skunk Industries'}
        ]
        
        result = filter_by_company_name(companies, '')
        
        assert len(result) == 2


class TestFilterByGoodsName:
    """Tests for filter_by_goods_name function."""
    
    def test_filter_by_good(self):
        """Test filtering companies by goods they produce"""
        companies = [
            {'name': 'Co1', 'goods': [{'Produced Goods': 'Steel'}, {'Produced Goods': 'Iron'}]},
            {'name': 'Co2', 'goods': [{'Produced Goods': 'Rations'}]},
            {'name': 'Co3', 'goods': [{'Produced Goods': 'Stainless Steel'}]}
        ]
        
        result = filter_by_goods_name(companies, 'Steel')
        
        assert len(result) == 2
        assert result[0]['name'] == 'Co1'
        assert result[1]['name'] == 'Co3'
    
    def test_case_insensitive(self):
        """Test that filtering is case-insensitive"""
        companies = [
            {'name': 'Co1', 'goods': [{'Produced Goods': 'Steel'}]},
            {'name': 'Co2', 'goods': [{'Produced Goods': 'Iron'}]}
        ]
        
        result = filter_by_goods_name(companies, 'steel')
        
        assert len(result) == 1
        assert result[0]['name'] == 'Co1'
    
    def test_no_match(self):
        """Test when no goods match"""
        companies = [
            {'name': 'Co1', 'goods': [{'Produced Goods': 'Steel'}]},
            {'name': 'Co2', 'goods': [{'Produced Goods': 'Iron'}]}
        ]
        
        result = filter_by_goods_name(companies, 'Copper')
        
        assert len(result) == 0
    
    def test_no_filter(self):
        """Test with empty search term returns all"""
        companies = [
            {'name': 'Co1', 'goods': [{'Produced Goods': 'Steel'}]},
            {'name': 'Co2', 'goods': [{'Produced Goods': 'Iron'}]}
        ]
        
        result = filter_by_goods_name(companies, '')
        
        assert len(result) == 2


class TestApplyAllFilters:
    """Tests for apply_all_filters function."""
    
    def test_combined_filters(self):
        """Test applying multiple filters together"""
        companies = [
            {
                'name': 'Flip Co',
                'professions': ['Agriculture'],
                'goods': [{'Produced Goods': 'Rations'}]
            },
            {
                'name': 'Skunk Industries',
                'professions': ['Metallurgy'],
                'goods': [{'Produced Goods': 'Steel'}]
            },
            {
                'name': 'Caboose Inc.',
                'professions': ['Manufacturing'],
                'goods': [{'Produced Goods': 'Circuits'}]
            }
        ]
        
        result = apply_all_filters(
            companies,
            professions=['Metallurgy'],
            company_search='Skunk',
            goods_search='Steel'
        )
        
        assert len(result) == 1
        assert result[0]['name'] == 'Skunk Industries'
    
    def test_no_filters(self):
        """Test with no filters applied returns all"""
        companies = [
            {'name': 'Co1', 'professions': ['Agriculture'], 'goods': [{'Produced Goods': 'Rations'}]},
            {'name': 'Co2', 'professions': ['Metallurgy'], 'goods': [{'Produced Goods': 'Steel'}]}
        ]
        
        result = apply_all_filters(companies, [], '', '')
        
        assert len(result) == 2
