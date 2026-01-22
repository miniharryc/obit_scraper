"""
Obituary scraper for Deaton Funeral Home website.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from typing import List, Dict, Optional
import re


class ObituaryScraper:
    """Scraper for extracting obituary information from Deaton Funeral Home website."""
    
    def __init__(self):
        self.base_url = "https://deatonfuneraljackson.com/wp/"
        self.obituaries_url = f"{self.base_url}obituaries/"
        self.session = requests.Session()
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_obituaries_page(self) -> Optional[BeautifulSoup]:
        """
        Fetch and parse the main obituaries page.
        
        Returns:
            BeautifulSoup object of the parsed page, or None if failed
        """
        try:
            response = self.session.get(self.obituaries_url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching obituaries page: {e}")
            return None
    
    def parse_date_range(self, date_text: str) -> Optional[Dict[str, datetime]]:
        """
        Parse date range text like "March 4, 1944 - January 21, 2026".
        
        Args:
            date_text: String containing birth and death dates
            
        Returns:
            Dictionary with 'birth_date' and 'death_date' keys, or None if parsing fails
        """
        try:
            # Split on dash and clean up whitespace
            parts = [part.strip() for part in date_text.split('-')]
            
            if len(parts) != 2:
                return None
                
            birth_date = parse_date(parts[0])
            death_date = parse_date(parts[1])
            
            return {
                'birth_date': birth_date,
                'death_date': death_date
            }
        except Exception as e:
            print(f"Error parsing dates from '{date_text}': {e}")
            return None
    
    def calculate_age_years(self, birth_date: datetime, death_date: datetime) -> int:
        """
        Calculate age in whole years (dropping months and days).
        
        Args:
            birth_date: Date of birth
            death_date: Date of death
            
        Returns:
            Age in whole years
        """
        age = death_date.year - birth_date.year
        
        # Subtract one year if death occurred before birthday in the death year
        if (death_date.month, death_date.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age
    
    def is_within_last_months(self, death_date: datetime, months: int = 3) -> bool:
        """
        Check if death date is within the last specified months.
        
        Args:
            death_date: Date of death
            months: Number of months to look back (default: 3)
            
        Returns:
            True if within the specified time range
        """
        cutoff_date = datetime.now() - timedelta(days=months * 30)  # Approximate
        return death_date >= cutoff_date
    
    def extract_obituary_info(self, soup: BeautifulSoup) -> List[Dict[str, any]]:
        """
        Extract obituary information from the parsed HTML.
        
        Args:
            soup: BeautifulSoup object of the obituaries page
            
        Returns:
            List of dictionaries containing obituary information
        """
        obituaries = []
        
        # Look for obituary entries - they seem to have names as links with dates
        obituary_links = soup.find_all('a', href=re.compile(r'/obituaries/'))
        
        for link in obituary_links:
            try:
                # Extract name from the link text
                name = link.get_text().strip()
                
                # Look for date information near the link
                # Check the parent element and siblings for date text
                parent = link.parent
                date_text = ""
                
                # Look for date pattern in the same element or nearby elements
                for element in [link, parent] + list(parent.find_all_next(limit=3)):
                    text = element.get_text() if element else ""
                    # Look for date pattern like "Month Day, Year - Month Day, Year"
                    date_match = re.search(r'([A-Za-z]+ \d+, \d{4})\s*-\s*([A-Za-z]+ \d+, \d{4})', text)
                    if date_match:
                        date_text = date_match.group(0)
                        break
                
                if not date_text:
                    # Alternative: look for separate date elements
                    date_elem = parent.find(text=re.compile(r'\d{4}'))
                    if date_elem:
                        date_text = date_elem.strip()
                
                if name and date_text:
                    dates = self.parse_date_range(date_text)
                    if dates:
                        age = self.calculate_age_years(dates['birth_date'], dates['death_date'])
                        
                        obituary_info = {
                            'name': name,
                            'birth_date': dates['birth_date'],
                            'death_date': dates['death_date'],
                            'age': age,
                            'date_text': date_text
                        }
                        
                        obituaries.append(obituary_info)
                        
            except Exception as e:
                print(f"Error processing obituary link: {e}")
                continue
        
        return obituaries
    
    def get_recent_obituaries(self, months: int = 3) -> List[Dict[str, any]]:
        """
        Get obituaries from the past specified months.
        
        Args:
            months: Number of months to look back (default: 3)
            
        Returns:
            List of obituary information dictionaries
        """
        soup = self.fetch_obituaries_page()
        if not soup:
            return []
        
        all_obituaries = self.extract_obituary_info(soup)
        
        # Filter for recent obituaries
        recent_obituaries = [
            obit for obit in all_obituaries 
            if self.is_within_last_months(obit['death_date'], months)
        ]
        
        # Sort by death date (most recent first)
        recent_obituaries.sort(key=lambda x: x['death_date'], reverse=True)
        
        return recent_obituaries
    
    def print_obituaries(self, obituaries: List[Dict[str, any]]) -> None:
        """
        Print obituary information in a formatted way.
        
        Args:
            obituaries: List of obituary information dictionaries
        """
        if not obituaries:
            print("No obituaries found for the specified time period.")
            return
            
        print(f"Found {len(obituaries)} obituaries from the past 3 months:\n")
        print("-" * 70)
        
        for obit in obituaries:
            print(f"Name: {obit['name']}")
            print(f"Date of Death: {obit['death_date'].strftime('%B %d, %Y')}")
            print(f"Age: {obit['age']} years")
            print("-" * 70)
