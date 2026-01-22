#!/usr/bin/env python3
"""
Debug script specifically for Breathitt Funeral Home CSS structure.
"""

from src.obituary_scraper import ObituaryScraper
import re

def debug_breathitt_structure():
    """Debug the actual HTML structure of Breathitt site"""
    scraper = ObituaryScraper()
    
    print("=== BREATHITT FUNERAL HOME CSS DEBUG ===")
    soup = scraper.fetch_page("https://www.thebreathittfuneralhome.com/obits")
    
    if soup:
        print("✓ Page fetched successfully\n")
        
        # Look for any elements containing "obit" in class name
        print("1. Elements with 'obit' in class name:")
        obit_elements = soup.find_all(class_=re.compile(r'obit', re.I))
        for i, elem in enumerate(obit_elements[:10]):  # First 10
            print(f"  {i+1}. Tag: {elem.name}, Class: {elem.get('class')}, Text: '{elem.get_text().strip()[:100]}'")
        
        # Look for any elements containing names we know exist
        print(f"\n2. Found {len(obit_elements)} elements with 'obit' in class")
        
        # Look for specific names from browser observation
        test_names = ["Roy Trent", "Beverly Stevens", "Mary Lou Crase"]
        page_text = soup.get_text()
        
        print(f"\n3. Checking for known names:")
        for name in test_names:
            if name in page_text:
                print(f"  ✓ Found '{name}' in page text")
                
                # Find the HTML element containing this name
                for elem in soup.find_all(string=re.compile(name, re.I)):
                    parent = elem.parent
                    if parent:
                        print(f"    Parent tag: {parent.name}")
                        print(f"    Parent class: {parent.get('class')}")
                        print(f"    Parent text: '{parent.get_text().strip()[:150]}'")
                        
                        # Check grandparent
                        grandparent = parent.parent
                        if grandparent:
                            print(f"    Grandparent tag: {grandparent.name}")
                            print(f"    Grandparent class: {grandparent.get('class')}")
                        print()
            else:
                print(f"  ✗ '{name}' not found in page text")
        
        # Look for date patterns and their surrounding HTML
        print(f"\n4. Looking for date patterns in HTML:")
        all_text_nodes = soup.find_all(string=re.compile(r'\d{4}'))
        date_contexts = []
        
        for text_node in all_text_nodes:
            if re.search(r'[A-Za-z]+ \d+, \d{4}', str(text_node)):
                parent = text_node.parent
                date_contexts.append((str(text_node).strip(), parent))
        
        print(f"Found {len(date_contexts)} text nodes with date patterns:")
        for i, (text, parent) in enumerate(date_contexts[:5]):
            print(f"  {i+1}. Text: '{text}'")
            print(f"     Parent tag: {parent.name if parent else 'None'}")
            print(f"     Parent class: {parent.get('class') if parent else 'None'}")
            print()

if __name__ == "__main__":
    debug_breathitt_structure()
