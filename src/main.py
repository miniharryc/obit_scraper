"""
Main module for the obituary scraper application.
"""

from obituary_scraper import ObituaryScraper


def main() -> None:
    """Main entry point for the obituary scraper application."""
    print("Multi-Funeral Home Obituary Scraper")
    print("=" * 50)
    print("Scraping: Deaton, Breathitt, and Watts Funeral Homes")
    print("Fetching obituaries from the past 3 months...\n")
    
    try:
        scraper = ObituaryScraper()
        obituaries = scraper.get_recent_obituaries(months=3)
        scraper.print_obituaries(obituaries)
        
    except Exception as e:
        print(f"An error occurred while scraping obituaries: {e}")
        print("Please check your internet connection and try again.")


if __name__ == "__main__":
    main()
