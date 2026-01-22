#!/usr/bin/env python3
"""
Debug script to test each funeral home individually.
"""

from src.obituary_scraper import ObituaryScraper
import re

def test_breathitt_extraction():
    """Test Breathitt extraction specifically"""
    scraper = ObituaryScraper()
    
    print("Testing Breathitt Funeral Home extraction...")
    soup = scraper.fetch_page("https://www.thebreathittfuneralhome.com/obits")
    
    if soup:
        print("✓ Page fetched successfully")
        
        # Look for date patterns
        page_text = soup.get_text()
        date_ranges = re.findall(r'([A-Za-z]+ \d+, \d{4})\s*-\s*([A-Za-z]+ \d+, \d{4})', page_text)
        
        print(f"Found {len(date_ranges)} date ranges:")
        for birth_str, death_str in date_ranges[:5]:  # Show first 5
            print(f"  {birth_str} - {death_str}")
        
        # Test extraction
        obits = scraper.extract_breathitt_obituaries(soup)
        print(f"\nExtracted {len(obits)} obituaries")
        
        for obit in obits[:3]:  # Show first 3
            print(f"  Name: {obit['name']}")
            print(f"  Death: {obit['death_date']}")
            print(f"  Age: {obit['age']}")
            print()
    else:
        print("✗ Failed to fetch page")

def test_watts_extraction():
    """Test Watts extraction specifically"""
    scraper = ObituaryScraper()
    
    print("Testing Watts Funeral Home extraction...")
    soup = scraper.fetch_page("https://www.wattsfuneralhomekentucky.com/obituaries/obituary-listings")
    
    if soup:
        print("✓ Page fetched successfully")
        
        # Look for date patterns
        page_text = soup.get_text()
        date_ranges = re.findall(r'([A-Za-z]+ \d+, \d{4})\s*-\s*([A-Za-z]+ \d+, \d{4})', page_text)
        
        print(f"Found {len(date_ranges)} date ranges:")
        for i, (birth_str, death_str) in enumerate(date_ranges[:3]):  # Show first 3
            date_range_str = f"{birth_str} - {death_str}"
            print(f"  {date_range_str}")
            
            # Debug name extraction for this date range
            date_pattern = re.escape(date_range_str)
            match = re.search(rf'(.{{0,200}}){date_pattern}', page_text, re.DOTALL)
            
            if match:
                preceding_text = match.group(1)
                print(f"    Preceding text: '{preceding_text[-100:]}'")  # Last 100 chars
                
                lines = preceding_text.split('\n')
                print(f"    Last 3 lines before date:")
                for line in lines[-3:]:
                    line = line.strip()
                    print(f"      '{line}'")
        
        # Test extraction
        obits = scraper.extract_watts_obituaries(soup)
        print(f"\nExtracted {len(obits)} obituaries")
        
        for obit in obits[:3]:  # Show first 3
            print(f"  Name: {obit['name']}")
            print(f"  Death: {obit['death_date']}")
            print(f"  Age: {obit['age']}")
            print()
    else:
        print("✗ Failed to fetch page")

if __name__ == "__main__":
    test_breathitt_extraction()
    print("\n" + "="*50 + "\n")
    test_watts_extraction()
