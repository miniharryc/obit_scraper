#!/usr/bin/env python3
"""
Detailed debug script to see exactly what's happening with name extraction.
"""

from src.obituary_scraper import ObituaryScraper
import re

def debug_watts_names():
    """Debug Watts name extraction in detail"""
    scraper = ObituaryScraper()
    
    print("=== WATTS FUNERAL HOME DEBUG ===")
    soup = scraper.fetch_page("https://www.wattsfuneralhomekentucky.com/obituaries/obituary-listings")
    
    if soup:
        page_text = soup.get_text()
        date_ranges = re.findall(r'([A-Za-z]+ \d+, \d{4})\s*-\s*([A-Za-z]+ \d+, \d{4})', page_text)
        
        print(f"Found {len(date_ranges)} date ranges")
        
        for i, (birth_str, death_str) in enumerate(date_ranges[:3]):
            date_range_str = f"{birth_str} - {death_str}"
            print(f"\n--- Date Range {i+1}: {date_range_str} ---")
            
            # Find text around this date range
            date_pattern = re.escape(date_range_str)
            match = re.search(rf'(.{{0,300}}){date_pattern}(.{{0,100}})', page_text, re.DOTALL)
            
            if match:
                before_text = match.group(1)
                after_text = match.group(2)
                
                print(f"Text before date: '{before_text[-200:]}'")
                print(f"Text after date: '{after_text[:100]}'")
                
                # Look at lines before
                lines = before_text.split('\n')
                print("\nLines before date:")
                for j, line in enumerate(lines[-5:]):
                    line = line.strip()
                    if line:
                        print(f"  Line {j}: '{line}' (len={len(line)})")
                        
                        # Test name criteria
                        meets_criteria = (
                            len(line) > 5 and len(line) < 60 and 
                            re.match(r'^[A-Z]', line) and 
                            ' ' in line and
                            not re.search(r'\d{4}|january|february|march|april|may|june|july|august|september|october|november|december', line.lower()) and
                            not re.search(r'view details|plant a tree|send flowers', line.lower())
                        )
                        print(f"    Meets name criteria: {meets_criteria}")

def debug_breathitt_dates():
    """Debug why Breathitt isn't finding date ranges"""
    scraper = ObituaryScraper()
    
    print("=== BREATHITT FUNERAL HOME DEBUG ===")
    soup = scraper.fetch_page("https://www.thebreathittfuneralhome.com/obits")
    
    if soup:
        page_text = soup.get_text()
        
        # Try different date patterns
        patterns = [
            r'([A-Za-z]+ \d+, \d{4})\s*-\s*([A-Za-z]+ \d+, \d{4})',  # Current pattern
            r'([A-Za-z]+ \d+, \d{4})\s*–\s*([A-Za-z]+ \d+, \d{4})',  # Em dash
            r'(\d+/\d+/\d{4})\s*-\s*(\d+/\d+/\d{4})',              # MM/DD/YYYY format
        ]
        
        for i, pattern in enumerate(patterns):
            matches = re.findall(pattern, page_text)
            print(f"Pattern {i+1} ({pattern}): {len(matches)} matches")
            for match in matches[:3]:
                print(f"  {match[0]} - {match[1]}")
        
        # Look for any mention of names from what I saw in browser
        test_names = ["Roy Trent", "Beverly Stevens", "Mary Lou Crase"]
        for name in test_names:
            if name in page_text:
                print(f"\nFound '{name}' in page text")
                # Find context around the name
                name_pattern = re.escape(name)
                match = re.search(rf'(.{{0,100}}){name_pattern}(.{{0,100}})', page_text, re.DOTALL)
                if match:
                    print(f"Context: '{match.group(1)[-50:]}{name}{match.group(2)[:50]}'")

if __name__ == "__main__":
    debug_breathitt_dates()
    print("\n" + "="*80 + "\n")
    debug_watts_names()
