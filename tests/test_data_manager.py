"""Tests for data management functions."""
import pytest
import pandas as pd
from gt_guild_app.core.data_manager import (
    feather_to_companies,
    companies_to_feather,
    prepare_goods_dataframe
)


class TestFeatherToCompanies:
    """Tests for feather_to_companies function."""
    
    def test_basic_conversion(self):
        """Test converting DataFrame to company structure"""
        df = pd.DataFrame({
            'company_name': ['Test Co', 'Test Co'],
            'industry': ['Manufacturing', 'Manufacturing'],
            'professions': ['Manufacturing', 'Manufacturing'],
            'timezone': ['UTC +00:00', 'UTC +00:00'],
            'local_time': ['12:00 PM', '12:00 PM'],
            'Produced Goods': ['Steel', 'Iron'],
            'Guildees Pay:': [90, 40],
            'Live EXC Price': [100, 50],
            'Live AVG Price': [95, 48],
            'Guild Max': [0, 0],
            'Guild Min': [0, 0],
            'Guild % Discount': [10, 20],
            'Guild Fixed Discount': [0, 0]
        })
        
        result = feather_to_companies(df)
        
        assert len(result) == 1
        assert result[0]['name'] == 'Test Co'
        assert result[0]['industry'] == 'Manufacturing'
        assert len(result[0]['goods']) == 2
        assert result[0]['goods'][0]['Produced Goods'] == 'Steel'
    
    def test_multiple_companies(self):
        """Test with multiple companies"""
        df = pd.DataFrame({
            'company_name': ['Co1', 'Co2'],
            'industry': ['Agriculture', 'Metallurgy'],
            'professions': ['Agriculture', 'Metallurgy'],
            'timezone': ['UTC -05:00', 'UTC +01:00'],
            'local_time': ['7:00 AM', '1:00 PM'],
            'Produced Goods': ['Rations', 'Steel'],
            'Guildees Pay:': [35, 90],
            'Live EXC Price': [43, 100],
            'Live AVG Price': [43, 95],
            'Guild Max': [0, 0],
            'Guild Min': [0, 0],
            'Guild % Discount': [20, 10],
            'Guild Fixed Discount': [0, 0]
        })
        
        result = feather_to_companies(df)
        
        assert len(result) == 2
        assert result[0]['name'] == 'Co1'
        assert result[1]['name'] == 'Co2'
    
    def test_profession_parsing(self):
        """Test parsing comma-separated professions"""
        df = pd.DataFrame({
            'company_name': ['Test Co'],
            'industry': ['Agriculture'],
            'professions': ['Agriculture, Food Production'],
            'timezone': ['UTC +00:00'],
            'local_time': ['12:00 PM'],
            'Produced Goods': ['Rations'],
            'Guildees Pay:': [35],
            'Live EXC Price': [43],
            'Live AVG Price': [43],
            'Guild Max': [0],
            'Guild Min': [0],
            'Guild % Discount': [20],
            'Guild Fixed Discount': [0]
        })
        
        result = feather_to_companies(df)
        
        assert len(result[0]['professions']) == 2
        assert 'Agriculture' in result[0]['professions']
        assert 'Food Production' in result[0]['professions']


class TestCompaniesToFeather:
    """Tests for companies_to_feather function."""
    
    def test_basic_conversion(self):
        """Test converting company structure to DataFrame"""
        companies = [
            {
                'name': 'Test Co',
                'industry': 'Manufacturing',
                'professions': ['Manufacturing'],
                'timezone': 'UTC +00:00',
                'local_time': '12:00 PM',
                'goods': [
                    {
                        'Produced Goods': 'Steel',
                        'Guildees Pay:': 90,
                        'Live EXC Price': 100,
                        'Live AVG Price': 95,
                        'Guild Max': 0,
                        'Guild Min': 0,
                        'Guild % Discount': 10,
                        'Guild Fixed Discount': 0
                    }
                ]
            }
        ]
        
        result = companies_to_feather(companies)
        
        assert len(result) == 1
        assert result.loc[0, 'company_name'] == 'Test Co'
        assert result.loc[0, 'Produced Goods'] == 'Steel'
    
    def test_multiple_goods(self):
        """Test company with multiple goods"""
        companies = [
            {
                'name': 'Test Co',
                'industry': 'Metallurgy',
                'professions': ['Metallurgy'],
                'timezone': 'UTC +00:00',
                'local_time': '12:00 PM',
                'goods': [
                    {'Produced Goods': 'Steel', 'Guildees Pay:': 90, 'Live EXC Price': 100,
                     'Live AVG Price': 95, 'Guild Max': 0, 'Guild Min': 0,
                     'Guild % Discount': 10, 'Guild Fixed Discount': 0},
                    {'Produced Goods': 'Iron', 'Guildees Pay:': 40, 'Live EXC Price': 50,
                     'Live AVG Price': 48, 'Guild Max': 0, 'Guild Min': 0,
                     'Guild % Discount': 20, 'Guild Fixed Discount': 0}
                ]
            }
        ]
        
        result = companies_to_feather(companies)
        
        assert len(result) == 2
        assert result.loc[0, 'Produced Goods'] == 'Steel'
        assert result.loc[1, 'Produced Goods'] == 'Iron'
    
    def test_empty_companies(self):
        """Test with empty companies list"""
        companies = []
        
        result = companies_to_feather(companies)
        
        assert len(result) == 0
        # Should still have correct columns
        expected_columns = [
            'company_name', 'industry', 'professions', 'timezone', 'local_time',
            'Produced Goods', 'Guildees Pay:', 'Live EXC Price', 'Live AVG Price',
            'Guild Max', 'Guild Min', 'Guild % Discount', 'Guild Fixed Discount'
        ]
        assert list(result.columns) == expected_columns


class TestPrepareGoodsDataframe:
    """Tests for prepare_goods_dataframe function."""
    
    def test_basic_preparation(self):
        """Test basic DataFrame preparation"""
        goods = [
            {
                'Produced Goods': 'Steel',
                'Guildees Pay:': 90.5,
                'Live EXC Price': 100,
                'Live AVG Price': 95,
                'Guild Max': 0,
                'Guild Min': 0,
                'Guild % Discount': 10,
                'Guild Fixed Discount': 0
            }
        ]
        
        result = prepare_goods_dataframe(goods)
        
        assert len(result) == 1
        assert result.loc[0, 'Produced Goods'] == 'Steel'
        assert result.loc[0, 'Guildees Pay:'] == 90.5
    
    def test_data_types(self):
        """Test that data types are correctly set"""
        goods = [
            {
                'Produced Goods': 'Steel',
                'Guildees Pay:': '90.5',  # String
                'Live EXC Price': '100',  # String
                'Live AVG Price': 95,
                'Guild Max': 0,
                'Guild Min': 0,
                'Guild % Discount': 10,
                'Guild Fixed Discount': 0
            }
        ]
        
        result = prepare_goods_dataframe(goods)
        
        assert result['Guildees Pay:'].dtype == 'float64'
        assert result['Live EXC Price'].dtype == 'int64'
        assert result['Produced Goods'].dtype == 'object'
    
    def test_empty_goods(self):
        """Test with empty goods list"""
        goods = []
        
        result = prepare_goods_dataframe(goods)
        
        assert len(result) == 0
        assert 'Produced Goods' in result.columns
        assert 'Guildees Pay:' in result.columns
    
    def test_handles_na_values(self):
        """Test handling of NA/None values"""
        goods = [
            {
                'Produced Goods': 'Steel',
                'Guildees Pay:': None,
                'Live EXC Price': None,
                'Live AVG Price': 95,
                'Guild Max': 0,
                'Guild Min': 0,
                'Guild % Discount': 10,
                'Guild Fixed Discount': 0
            }
        ]
        
        result = prepare_goods_dataframe(goods)
        
        # NaN/None should be converted to 0
        assert result.loc[0, 'Guildees Pay:'] == 0.0
        assert result.loc[0, 'Live EXC Price'] == 0
