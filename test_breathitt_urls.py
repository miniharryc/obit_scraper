#!/usr/bin/env python3
"""
Test script to check Breathitt obit_path values to fix URL construction.
"""

import requests

def test_breathitt_url_construction():
    """Test what the obit_path field actually contains"""
    
    print("=== TESTING BREATHITT URL CONSTRUCTION ===")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    try:
        # Step 1: Establish session
        regular_url = "https://www.thebreathittfuneralhome.com/obits"
        regular_response = session.get(regular_url, timeout=20)
        
        if regular_response.status_code == 200:
            print("✓ Session established")
            
            # Step 2: Get JSON data
            json_url = "https://www.thebreathittfuneralhome.com/obituaries/obit_json?page_count=5&page_number=1&search_field=&sort_by=deathDate&sort_direction=desc"
            
            json_headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': regular_url
            }
            
            response = session.get(json_url, headers=json_headers, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    print(f"Found {len(data)} obituaries")
                    
                    # Check first 3 obituaries
                    for i, obit in enumerate(data[:3]):
                        first_name = obit.get('first_name', '')
                        last_name = obit.get('last_name', '')
                        obit_path = obit.get('obit_path', '')
                        
                        print(f"\n--- Obituary {i+1}: {first_name} {last_name} ---")
                        print(f"Raw obit_path: '{obit_path}'")
                        
                        # Analyze the obit_path format
                        if obit_path.startswith('http'):
                            print(f"  → Already a full URL")
                            final_url = obit_path
                        elif obit_path.startswith('/'):
                            print(f"  → Relative path, needs base URL")
                            final_url = f"https://www.thebreathittfuneralhome.com{obit_path}"
                        else:
                            print(f"  → Unexpected format")
                            final_url = f"https://www.thebreathittfuneralhome.com/{obit_path}"
                        
                        print(f"Final URL: {final_url}")
                else:
                    print("No obituary data found")
            else:
                print(f"JSON API failed: {response.status_code}")
        else:
            print(f"Session establishment failed: {regular_response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_breathitt_url_construction()
