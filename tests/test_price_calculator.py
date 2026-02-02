"""Tests for price calculation functions."""
import pytest
import pandas as pd
from gt_guild_app.business.price_calculator import (
    calculate_guildees_pay,
    apply_price_bounds,
    smart_round_price,
    update_live_prices,
    calculate_all_guildees_prices
)


class TestSmartRoundPrice:
    """Tests for smart_round_price function."""
    
    def test_tier1_under_100(self):
        """Prices under $100 round to nearest 0.5"""
        assert smart_round_price(45.2) == 45.0
        assert smart_round_price(45.6) == 45.5
        assert smart_round_price(45.8) == 46.0
    
    def test_tier2_100_to_500(self):
        """Prices $100-$500 round to nearest $1"""
        assert smart_round_price(245.3) == 245
        assert smart_round_price(245.7) == 246
    
    def test_tier3_500_to_1000(self):
        """Prices $500-$1000 round to nearest $5"""
        assert smart_round_price(678.3) == 680
        assert smart_round_price(681.3) == 680
    
    def test_tier4_1000_to_5000(self):
        """Prices $1000-$5000 round to nearest $10"""
        assert smart_round_price(1234.5) == 1230
        assert smart_round_price(1237.5) == 1240
    
    def test_tier5_5000_to_10000(self):
        """Prices $5000-$10000 round to nearest $50"""
        assert smart_round_price(6789.0) == 6800
        assert smart_round_price(6724.0) == 6700
    
    def test_tier6_10000_to_50000(self):
        """Prices $10000-$50000 round to nearest $100"""
        assert smart_round_price(12345.0) == 12300
        assert smart_round_price(12367.0) == 12400
    
    def test_tier7_above_50000(self):
        """Prices above $50000 round to nearest $500"""
        assert smart_round_price(67890.0) == 68000
        assert smart_round_price(67249.0) == 67000
    
    def test_edge_cases(self):
        """Test edge cases"""
        assert smart_round_price(0) == 0
        assert smart_round_price(99.9) == 100.0
        assert smart_round_price(100.0) == 100


class TestCalculateGuildeesPay:
    """Tests for calculate_guildees_pay function."""
    
    def test_basic_discount(self):
        """Test basic percentage discount"""
        result = calculate_guildees_pay(100, 10)
        assert result == 90.0
    
    def test_no_discount(self):
        """Test with 0% discount"""
        result = calculate_guildees_pay(100, 0)
        assert result == 100.0
    
    def test_large_discount(self):
        """Test with large discount"""
        result = calculate_guildees_pay(1000, 50)
        assert result == 500.0
    
    def test_with_rounding(self):
        """Test that result is properly rounded"""
        result = calculate_guildees_pay(43, 20)
        # 43 * 0.8 = 34.4, should round to 34.5
        assert result == 34.5


class TestApplyPriceBounds:
    """Tests for apply_price_bounds function."""
    
    def test_within_bounds(self):
        """Price within min/max stays unchanged"""
        assert apply_price_bounds(100, 50, 150) == 100
    
    def test_below_min(self):
        """Price below min gets capped to min"""
        assert apply_price_bounds(40, 50, 150) == 50
    
    def test_above_max(self):
        """Price above max gets capped to max"""
        assert apply_price_bounds(200, 50, 150) == 150
    
    def test_zero_bounds(self):
        """Zero bounds means no capping"""
        assert apply_price_bounds(100, 0, 0) == 100
        assert apply_price_bounds(1000, 0, 0) == 1000


class TestUpdateLivePrices:
    """Tests for update_live_prices function."""
    
    def test_update_with_price_data(self):
        """Test updating DataFrame with live price data"""
        goods_df = pd.DataFrame({
            'Produced Goods': ['Steel', 'Iron'],
            'Live EXC Price': [0, 0],
            'Live AVG Price': [0, 0]
        })
        
        price_data = {
            'Steel': {'currentPrice': 100, 'avgPrice': 95},
            'Iron': {'currentPrice': 50, 'avgPrice': 48}
        }
        
        result = update_live_prices(goods_df, price_data)
        
        assert result.loc[0, 'Live EXC Price'] == 100
        assert result.loc[0, 'Live AVG Price'] == 95
        assert result.loc[1, 'Live EXC Price'] == 50
        assert result.loc[1, 'Live AVG Price'] == 48
    
    def test_update_with_missing_material(self):
        """Test handling of materials not in price data"""
        goods_df = pd.DataFrame({
            'Produced Goods': ['UnknownMaterial'],
            'Live EXC Price': [0],
            'Live AVG Price': [0]
        })
        
        price_data = {'Steel': {'currentPrice': 100, 'avgPrice': 95}}
        
        result = update_live_prices(goods_df, price_data)
        
        # Should remain 0 for unknown material
        assert result.loc[0, 'Live EXC Price'] == 0
        assert result.loc[0, 'Live AVG Price'] == 0


class TestCalculateAllGuildeesPrices:
    """Tests for calculate_all_guildees_prices function."""
    
    def test_calculate_all(self):
        """Test calculating guildees pay for all rows"""
        goods_df = pd.DataFrame({
            'Produced Goods': ['Steel', 'Iron'],
            'Live EXC Price': [100, 50],
            'Guild % Discount': [10, 20],
            'Guild Max': [0, 0],
            'Guild Min': [0, 0],
            'Guildees Pay:': [0, 0]
        })
        
        result = calculate_all_guildees_prices(goods_df)
        
        # Steel: 100 * 0.9 = 90
        assert result.loc[0, 'Guildees Pay:'] == 90.0
        # Iron: 50 * 0.8 = 40
        assert result.loc[1, 'Guildees Pay:'] == 40.0
    
    def test_with_bounds(self):
        """Test with min/max bounds applied"""
        goods_df = pd.DataFrame({
            'Produced Goods': ['Steel'],
            'Live EXC Price': [100],
            'Guild % Discount': [50],
            'Guild Max': [60],
            'Guild Min': [0],
            'Guildees Pay:': [0]
        })
        
        result = calculate_all_guildees_prices(goods_df)
        
        # 100 * 0.5 = 50, but max is 60, so should be 50
        assert result.loc[0, 'Guildees Pay:'] == 50.0
