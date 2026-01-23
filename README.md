# Multi-Funeral Home Obituary Scraper

A Python application that scrapes obituary information from multiple Kentucky funeral home websites.

## Features

This application scrapes obituary information from **three funeral homes** and extracts:

- **Name of the deceased**
- **Date of death** 
- **Age in whole years** (drops months and days)
- **Funeral home source** (which funeral home published the obituary)
- **Filters for the past 3 months** of obituaries
- **Combined and sorted by death date** (newest first, reverse chronological)

## Supported Funeral Homes

1. **Deaton Funeral Home** - Jackson, KY
   - URL: https://deatonfuneraljackson.com/wp/obituaries/
   - Method: Individual page visits for complete birth-death date ranges

2. **Breathitt Funeral Home** - Jackson, KY  
   - URL: https://www.thebreathittfuneralhome.com/obits
   - Method: Main page extraction with date range parsing

3. **Watts Funeral Home** - Hazard, KY
   - URL: https://www.wattsfuneralhomekentucky.com/obituaries/obituary-listings
   - Method: Main page extraction with date range parsing

## Project Structure

```
python_workspace/
├── src/                         # Source code
│   ├── __init__.py             # Package initialization
│   ├── main.py                 # Main application entry point
│   └── obituary_scraper.py     # Obituary scraper class
├── tests/                      # Test files
│   ├── __init__.py             # Test package initialization
│   └── test_main.py            # Tests for scraper functionality
├── docs/                       # Documentation
├── venv/                       # Virtual environment
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
└── README.md                   # This file
```

## Setup

### 1. Activate Virtual Environment

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

## Usage

### Running the Main Module

```bash
python src/main.py
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html
```

### Code Formatting and Linting

```bash
# Format code with Black
black src/ tests/

# Lint code with Flake8
flake8 src/ tests/

# Type checking with MyPy
mypy src/
```

## Development

1. Make sure to activate the virtual environment before working
2. Install development dependencies for testing and code quality tools
3. Write tests for new functionality in the `tests/` directory
4. Follow PEP 8 style guidelines
5. Add type hints to your functions

## Author

- **Harold Combs** - harryc@hey.com

## License

This project is open source and available under the [MIT License](LICENSE).
