# Google Maps Directory Scraper

This is a simple and powerful tool for extracting business information from Google Maps. By entering a city name and business category, you can get a clean, organized list of businesses in an Excel file.

## Prerequisites

Before running the application, make sure you have the following installed on your system:
1. **Python** version 3.10 or higher

## Installation and Setup

First, clone or download the project and open its folder.
Then, open your terminal (Terminal / CMD / PowerShell) in the project directory and run the following commands to install the dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

## How to Use

This tool features a simple and modern web-based user interface. To run it, enter the following command in your terminal:

```bash
streamlit run app.py
```

After running this command, a web page will open in your browser. On this page:
1. **City:** Enter your desired city name (e.g., New York, Isfahan).
2. **Business Category:** Enter the type of business (e.g., Restaurant, Accounting firm).
3. Click the **Start Scraping** button.

The scraper will automatically open a browser and collect information for all relevant businesses.

## Output

Once finished, an Excel file containing the following information will be ready for download:
- Business Name
- Rating
- Review Count
- Category
- Address
- Phone Number
- Website URL
- Open Status

You can download the output file directly from the web page by clicking the "Download Excel File" button.
