"""
Obituary scraper for Deaton Funeral Home website.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from typing import List, Dict, Optional
import re
import time


class ObituaryScraper:
    """Scraper for extracting obituary information from multiple funeral home websites."""
    
    def __init__(self):
        # Define all funeral home URLs
        self.funeral_homes = {
            'Deaton Funeral Home': "https://deatonfuneraljackson.com/wp/obituaries/",
            'Breathitt Funeral Home': "https://www.thebreathittfuneralhome.com/obits",
            'Watts Funeral Home': "https://www.wattsfuneralhomekentucky.com/obituaries/obituary-listings"
        }
        
        self.session = requests.Session()
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object of the parsed page, or None if failed
        """
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching page {url}: {e}")
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
        except Exception:
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
    
    def fetch_obituary_detail(self, obituary_url: str) -> Optional[Dict[str, any]]:
        """
        Fetch detailed obituary information from individual obituary page.
        
        Args:
            obituary_url: URL of the individual obituary page
            
        Returns:
            Dictionary with birth_date and death_date, or None if parsing fails
        """
        try:
            response = self.session.get(obituary_url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for date range in the obituary page content
            page_text = soup.get_text()
            
            # Look for pattern like "March 4, 1944 - January 21, 2026"
            date_match = re.search(r'([A-Za-z]+ \d+, \d{4})\s*-\s*([A-Za-z]+ \d+, \d{4})', page_text)
            if date_match:
                return self.parse_date_range(date_match.group(0))
            
            return None
            
        except Exception:
            return None

    def extract_deaton_obituaries(self, soup: BeautifulSoup) -> List[Dict[str, any]]:
        """Extract obituaries from Deaton Funeral Home (requires individual page visits)."""
        obituaries = []
        processed_links = set()
        
        obituary_name_links = []
        all_links = soup.find_all('a')
        
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text().strip()
            
            if ('/obituaries/' in href and 
                href not in processed_links and
                not re.match(r'^[A-Za-z]+ \d+, \d{4}$', text) and
                len(text) > 3 and
                not text.isdigit()):
                
                obituary_name_links.append((text, href))
                processed_links.add(href)
        
        for name, obituary_url in obituary_name_links[:20]:
            try:
                dates = self.fetch_obituary_detail(obituary_url)
                if dates:
                    age = self.calculate_age_years(dates['birth_date'], dates['death_date'])
                    obituaries.append({
                        'name': name.strip(),
                        'birth_date': dates['birth_date'],
                        'death_date': dates['death_date'],
                        'age': age,
                        'funeral_home': 'Deaton Funeral Home',
                        'url': obituary_url
                    })
            except Exception:
                continue
        
        return obituaries

    def extract_breathitt_obituaries(self, soup: BeautifulSoup = None) -> List[Dict[str, any]]:
        """Extract obituaries from Breathitt Funeral Home using JSON API with session."""
        obituaries = []
        
        regular_url = "https://www.thebreathittfuneralhome.com/obits"
        json_url = "https://www.thebreathittfuneralhome.com/obituaries/obit_json?page_count=20&page_number=1&search_field=&sort_by=deathDate&sort_direction=desc"

        # Endpoint returns HTML instead of JSON without these AJAX headers
        json_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': regular_url
        }

        # Retry once — the endpoint occasionally fails transiently
        data = None
        for attempt in range(2):
            if attempt > 0:
                time.sleep(5)
            try:
                # Step 1: Visit regular page to establish session
                regular_response = self.session.get(regular_url, timeout=20)

                if regular_response.status_code != 200:
                    print(f"    Failed to establish session with Breathitt (status: {regular_response.status_code})")
                    continue

                # Step 2: Use JSON API with established session
                response = self.session.get(json_url, headers=json_headers, timeout=20)

                if response.status_code == 403 and 'cloudflare' in response.headers.get('server', '').lower():
                    print(f"    Breathitt JSON API blocked by Cloudflare bot protection (403)")
                    continue

                if response.status_code != 200:
                    print(f"    Breathitt JSON API returned status: {response.status_code}")
                    continue

                data = response.json()
                break
            except ValueError:
                print(f"    Breathitt returned non-JSON response: {response.text[:200]!r}")
            except Exception as e:
                print(f"    Error fetching data from Breathitt: {e}")

        if data is None:
            return obituaries

        # JSON response is a list of obituaries directly
        if not isinstance(data, list):
            print(f"    Unexpected JSON response format from Breathitt")
            return obituaries

        for obit_data in data:
            try:
                # Build name from components
                first_name = obit_data.get('first_name', '').strip()
                middle_name = obit_data.get('middle_name', '').strip()
                last_name = obit_data.get('last_name', '').strip()

                # Combine name parts
                name_parts = [first_name, middle_name, last_name]
                name = ' '.join([part for part in name_parts if part])

                birth_date_str = obit_data.get('birth_date', '')
                death_date_str = obit_data.get('death_date', '')

                if name and birth_date_str and death_date_str:
                    # Parse dates (MM/DD/YYYY format)
                    birth_date = parse_date(birth_date_str)
                    death_date = parse_date(death_date_str)
                    age = self.calculate_age_years(birth_date, death_date)

                    # Use obit_path - it's already a full URL
                    full_url = obit_data.get('obit_path', '')

                    obituaries.append({
                        'name': name,
                        'birth_date': birth_date,
                        'death_date': death_date,
                        'age': age,
                        'funeral_home': 'Breathitt Funeral Home',
                        'url': full_url
                    })
            except Exception as e:
                print(f"    Error parsing obituary data: {e}")
                continue

        return obituaries

    def extract_watts_obituaries(self, soup: BeautifulSoup) -> List[Dict[str, any]]:
        """Extract obituaries from Watts Funeral Home using CSS selectors."""
        obituaries = []
        
        # Find all obituary info containers
        obituary_info_divs = soup.find_all(class_=re.compile(r'obituary-info'))
        
        for obituary_div in obituary_info_divs:
            try:
                # Look for name element within obituary-info
                name_element = obituary_div.find(class_=re.compile(r'name')) or obituary_div.find('h2') or obituary_div.find('h3')
                
                if name_element:
                    name = name_element.get_text().strip()
                    
                    # Look for date range in the obituary div
                    div_text = obituary_div.get_text()
                    date_match = re.search(r'([A-Za-z]+ \d+, \d{4})\s*[-–—]\s*([A-Za-z]+ \d+, \d{4})', div_text)
                    
                    # Look for a link to the individual obituary page
                    obituary_url = ''
                    link_element = obituary_div.find('a', href=True)
                    if link_element:
                        href = link_element.get('href', '')
                        if href.startswith('/'):
                            obituary_url = f"https://www.wattsfuneralhomekentucky.com{href}"
                        elif href.startswith('http'):
                            obituary_url = href
                    
                    if date_match:
                        dates = self.parse_date_range(f"{date_match.group(1)} - {date_match.group(2)}")
                        if dates:
                            age = self.calculate_age_years(dates['birth_date'], dates['death_date'])
                            obituaries.append({
                                'name': name,
                                'birth_date': dates['birth_date'], 
                                'death_date': dates['death_date'],
                                'age': age,
                                'funeral_home': 'Watts Funeral Home',
                                'url': obituary_url
                            })
            except Exception:
                continue
                
        return obituaries

    def get_recent_obituaries(self, months: int = 3) -> List[Dict[str, any]]:
        """
        Get obituaries from all funeral homes for the past specified months.
        
        Args:
            months: Number of months to look back (default: 3)
            
        Returns:
            List of obituary information dictionaries, sorted by death date (newest first)
        """
        all_obituaries = []
        
        print("Fetching obituaries from all funeral homes...")
        
        # Fetch from each funeral home
        for home_name, url in self.funeral_homes.items():
            print(f"Checking {home_name}...")
            try:
                soup = self.fetch_page(url)
                if soup:
                    print(f"  Successfully fetched page for {home_name}")
                    if 'deatonfuneraljackson' in url:
                        print(f"  Extracting from Deaton...")
                        obits = self.extract_deaton_obituaries(soup)
                    elif 'thebreathittfuneralhome' in url:
                        print(f"  Extracting from Breathitt...")
                        obits = self.extract_breathitt_obituaries(soup)
                    elif 'wattsfuneralhomekentucky' in url:
                        print(f"  Extracting from Watts...")
                        obits = self.extract_watts_obituaries(soup)
                    else:
                        obits = []
                    
                    print(f"  Found {len(obits)} obituaries from {home_name}")
                    all_obituaries.extend(obits)
                else:
                    print(f"  Failed to fetch page for {home_name}")
            except Exception as e:
                print(f"  Error processing {home_name}: {e}")
        
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
        print("-" * 80)
        
        for obit in obituaries:
            print(f"Name: {obit['name']}")
            print(f"Date of Death: {obit['death_date'].strftime('%B %d, %Y')}")
            print(f"Age: {obit['age']} years")
            print(f"Funeral Home: {obit['funeral_home']}")
            if obit.get('url'):
                print(f"Obituary URL: {obit['url']}")
            print("-" * 80)
