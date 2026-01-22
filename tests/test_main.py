"""
Tests for the obituary scraper module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from datetime import datetime
from obituary_scraper import ObituaryScraper


class TestObituaryScraper:
    """Test cases for ObituaryScraper class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.scraper = ObituaryScraper()
    
    def test_scraper_initialization(self):
        """Test that scraper initializes correctly."""
        assert self.scraper.base_url == "https://deatonfuneraljackson.com/wp/"
        assert self.scraper.obituaries_url == "https://deatonfuneraljackson.com/wp/obituaries/"
        assert self.scraper.session is not None
    
    def test_parse_date_range_valid(self):
        """Test parsing valid date range."""
        date_text = "March 4, 1944 - January 21, 2026"
        result = self.scraper.parse_date_range(date_text)
        
        assert result is not None
        assert result['birth_date'].year == 1944
        assert result['birth_date'].month == 3
        assert result['birth_date'].day == 4
        assert result['death_date'].year == 2026
        assert result['death_date'].month == 1
        assert result['death_date'].day == 21
    
    def test_parse_date_range_invalid(self):
        """Test parsing invalid date range."""
        result = self.scraper.parse_date_range("Invalid date text")
        assert result is None
    
    def test_calculate_age_years(self):
        """Test age calculation in whole years."""
        birth_date = datetime(1944, 3, 4)
        death_date = datetime(2026, 1, 21)
        
        age = self.scraper.calculate_age_years(birth_date, death_date)
        assert age == 81  # Death occurred before 82nd birthday
    
    def test_calculate_age_years_after_birthday(self):
        """Test age calculation when death occurs after birthday in death year."""
        birth_date = datetime(1944, 3, 4)
        death_date = datetime(2026, 5, 21)  # After March 4th
        
        age = self.scraper.calculate_age_years(birth_date, death_date)
        assert age == 82
    
    def test_is_within_last_months_recent(self):
        """Test date filtering for recent dates."""
        recent_date = datetime.now()
        assert self.scraper.is_within_last_months(recent_date, 3) is True
    
    def test_is_within_last_months_old(self):
        """Test date filtering for old dates."""
        old_date = datetime(2020, 1, 1)
        assert self.scraper.is_within_last_months(old_date, 3) is False
