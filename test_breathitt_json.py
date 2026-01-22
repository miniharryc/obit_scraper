#!/usr/bin/env python3
"""
Test script specifically for Breathitt JSON API.
"""

import requests
import json
from dateutil.parser import parse as parse_date

def test_breathitt_json():
    """Test the Breathitt JSON API with proper session setup"""
    
    print("=== TESTING BREATHITT JSON API ===")
    
    regular_url = "https://www.thebreathittfuneralhome.com/obits"
    json_url = "https://www.thebreathittfuneralhome.com/obituaries/obit_json?page_count=20&page_number=1&search_field=&sort_by=deathDate&sort_direction=desc"
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Step 1: Visit the regular obituaries page to establish session/cookies
        print("Step 1: Visiting regular obituaries page to establish session...")
        print(f"Fetching: {regular_url}")
        
        regular_response = session.get(regular_url, timeout=10)
        print(f"Regular page response status: {regular_response.status_code}")
        
        if regular_response.status_code == 200:
            print(f"✓ Successfully fetched regular page")
            print(f"Cookies received: {len(session.cookies)} cookies")
            
            # Show some cookies for debugging
            for cookie in session.cookies:
                print(f"  Cookie: {cookie.name}={cookie.value[:20]}...")
                
            # Check response headers for additional info
            print(f"Response headers: {dict(regular_response.headers)}")
        
        # Step 2: Now try the JSON API with the established session
        print(f"\nStep 2: Trying JSON API with established session...")
        print(f"Fetching: {json_url}")
        
        # Add additional headers that might be needed
        json_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': regular_url
        }
        
        response = session.get(json_url, headers=json_headers, timeout=10)
        print(f"JSON API response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if data is a list or dict
            if isinstance(data, list):
                print(f"JSON response is a list with {len(data)} items")
                obituaries = data
            elif isinstance(data, dict):
                print(f"JSON response is a dict with keys: {list(data.keys())}")
                if 'obituaries' in data:
                    obituaries = data['obituaries']
                else:
                    obituaries = []
                    print("No 'obituaries' key found in dict")
            else:
                print(f"Unexpected JSON response type: {type(data)}")
                obituaries = []
            
            if obituaries:
                print(f"Found {len(obituaries)} obituaries in JSON")
                
                # Show first few obituaries
                for i, obit in enumerate(obituaries[:5]):
                    print(f"\n--- Obituary {i+1} ---")
                    print(f"Available keys: {list(obit.keys())}")
                    
                    # Try different possible field names
                    name_fields = ['full_name', 'name', 'firstName', 'lastName', 'deceasedName']
                    birth_fields = ['birth_date', 'birthDate', 'dateOfBirth', 'born']
                    death_fields = ['death_date', 'deathDate', 'dateOfDeath', 'died']
                    
                    name = None
                    for field in name_fields:
                        if field in obit and obit[field]:
                            name = obit[field]
                            print(f"Name (from {field}): {name}")
                            break
                    
                    birth_date = None
                    for field in birth_fields:
                        if field in obit and obit[field]:
                            birth_date = obit[field]
                            print(f"Birth date (from {field}): {birth_date}")
                            break
                    
                    death_date = None
                    for field in death_fields:
                        if field in obit and obit[field]:
                            death_date = obit[field]
                            print(f"Death date (from {field}): {death_date}")
                            break
                    
                    # Show all fields for debugging
                    print(f"All data: {json.dumps(obit, indent=2)[:200]}...")
                    
            else:
                print("No 'obituaries' key in JSON response")
                print(f"Raw JSON (first 500 chars): {str(data)[:500]}")
                
        else:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response content: {response.text[:500]}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_breathitt_json()
